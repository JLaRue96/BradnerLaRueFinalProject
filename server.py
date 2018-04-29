import socket
import sys
import time
import pickle
import json
from constants import initial_earnings
from deck_util import generate_deck
from deck_util import shuffle_deck
from deck_util import remove_card_from_top
from handle_game import compare_hands
from handle_game import get_hand_value
from player import Player


class HoldEmServer:

    def __init__(self):
        self.client_list = []
        self.HOST = ''
        self.PORT = 8888
        self.num_players = 1
        self.addresses = {}
        self.sockets = {}
        self.conn = {}
        self.addr = {}

        # Global information regarding how much money is on the table.
        self.pot = 0

        # Global list of players
        # Format: [Player, Player, ...]
        self.player_list = []

        # Global list of cards.
        # Format: [(Rank, Suit), (Rank, Suit), ...]
        self.table_card_list = []

        try:
            for i in range(self.num_players):
                self.sockets[i] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("socket created")
                self.sockets[i].bind((self.HOST, self.PORT + i))
        except socket.error:
            print("failed to create socket")
            sys.exit();

    def shutDown(self):
        for i in range(self.num_players):
            self.sockets[i].close()

    def acceptClients(self):
        #listen for 2 players
        for i in range(self.num_players):
            self.sockets[i].listen(1)
            self.conn[i], self.addr[i] = self.sockets[i].accept()
            print("connection " + str(i + 1) + " of " + str(self.num_players) + " established.")

    def collectCommand(self, stateMsg, options, playerNum):
        data = {"message" : stateMsg, "options" : options}

        self.sendDict(data, playerNum)

        dictIn = self.getResponse(playerNum)
        
        print("client selection: " + dictIn["selection"])

        return dictIn

    def getResponse(self, playerNum):
        newData = False
        while not newData:
            dataIn = self.conn[playerNum].recv(4096)
            if dataIn:
                newData = True

        dictIn = pickle.loads(dataIn)

        return dictIn

    def sendDict(self, dict, playerNum):
        pickledObj = pickle.dumps(dict, -1)
        self.conn[playerNum].sendall(pickledObj)
        return True

    def unpack_data(self, data):
        new_dict = pickle.loads(data)
        return new_dict

    def pack_dict(self, dict):
        data = pickle.dumps(dict)

    def send_message(self, message, player_num):
        """
        Sends a message to a particular player.
        :param message: Message in string form.
        :param player_num: ID of the player
        """
        self.collectCommand(message, [], player_num)

    def send_message_all(self, message):
        """
        Sends a message to every client connected to server.
        :param message: Message in string form.
        """
        for i in range(self.num_players):
            self.collectCommand(message, [], i)

    def play_round(self):
        """
        Plays a round of Hold'em.
        Assumes that all players will remain in the game
        for the duration of the round.
        :return:
        """

        # Load and shuffle the deck
        deck = shuffle_deck(generate_deck())

        # Reset the table_card_list if it currently
        # contains cards.
        self.table_card_list = []

        # Gives two cards to each of the players.
        for player in self.player_list:
            first_card = remove_card_from_top(deck)
            second_card = remove_card_from_top(deck)
            hand = [first_card, second_card]

            player.set_hand(hand)

        cards_on_table = self.get_table_list_string()

        # Tells players what cards are on the table.
        self.send_message_all(cards_on_table)

        # Sends information to the player about their current hands.
        for i in range(self.num_players):
            """
            PSEUDO:
            
            -get player instance from i (pid)
            -get hand from player
            -formulate a string 
            """

        """
        # TODO: for each client, send from server to
        # client a string of each card name and rank.

        # TODO: Each Client bets. Clients can also fold if need be.

        # Play the flop cards.
        flop_ctr = 0
        remove_card_from_top(deck)
        while flop_ctr < 3:
            card = remove_card_from_top(deck)
            self.table_card_list.append(card)
            flop_ctr += 1

        # TODO: Send Clients list of cards. Should be printed to terminal.
        # TODO: Each Client bets. Clients can also fold if need be.

        # Play the turn card.
        remove_card_from_top(deck)
        turn_card = remove_card_from_top(deck)
        self.table_card_list.append(turn_card)

        # TODO: Send Clients list of cards. Should be printed to terminal.
        # TODO: Each Client bets. Clients can also fold if need be.

        # Play the river card.
        remove_card_from_top(deck)
        river_card = remove_card_from_top(deck)
        self.table_card_list.append(river_card)

        # TODO: Send Clients list of cards. Should be printed to terminal.
        # TODO: Each Client bets. Clients can also fold if need be.

        player_info_tuple_list = []

        # Get Player info tuples.
        # Tuple format: (Player ID, Player's hand value, highest rank of Player's hand value)
        for player in self.player_list:

            if player.has_not_folded():

                hand_value = get_hand_value(player.get_hand(), self.table_card_list)

                if hand_value[0] == 'Two pair':
                    player_tup = (player.get_id(), hand_value[0], hand_value[1], hand_value[2], hand_value[3])
                elif hand_value[0] == 'nothing':
                    player_tup = (player.get_id(), hand_value[0], hand_value[1])
                else:
                    player_tup = (player.get_id(), hand_value[0], hand_value[1], hand_value[2])

                player_info_tuple_list.append(player_tup)

        # Get a list of winners from the player info tuples:
        winners = compare_hands(player_info_tuple_list)

        # TODO: Send to clients the list of winners.
        # TODO: Distribute pot values winners.

        self.reset_player_statuses()
        
        """

    def handle_betting(self):
        """
        players will now bet. During this time,
        players have the opportunity to bet, fold, raise, or call.
        """
        pass

    def get_table_list_string(self):
        """
        Creates a string of the list of cards on the table.
        :return: String of table card list.
        """
        card_list_str = ''
        card_list_str += '\nCARDS ON TABLE:\n'

        for card in self.table_card_list:
            card_list_str += card[0] + ' of ' + card[1] + '\n'

        return card_list_str

    def reset_player_statuses(self):
        """
        Updates the player statuses so that
        each player is in play mode.
        :return: None
        """
        for player in self.player_list:
            player.reset_is_playing_status()

    def initialize_player(self, pid):
        """
        Initializes a player.
        Updates the player list to handle this.
        :param pid: player_id
        """

        new_player = Player(pid, initial_earnings, True)

        self.player_list.append(new_player)

    def get_player_from_id(self, pid):
        """
        Gets the player from a given player id
        :param pid: player_id
        :return: Player instance.
        """
        for player in self.player_list:
            if player.get_id() == pid:
                return player


myServer = HoldEmServer()
myServer.acceptClients()
# test sending of data here
players_present = True

while players_present:
    myServer.collectCommand("Start a new round?", ["start", "quit"], 0)
    myServer.play_round()

myServer.collectCommand("test game state", ["bet", "fold"], 0)   
time.sleep(5)
myServer.shutDown()
