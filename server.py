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
        self.num_players = 2
        self.addresses = {}
        self.sockets = {}
        self.conn = {}
        self.addr = {}

        # Global flag to determine if somebody has folded.
        self.has_folded = False

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
            self.initialize_player(i)

    def collectCommand(self, stateMsg, options, playerNum):
        data = {"message" : stateMsg, "options" : options}

        self.sendDict(data, playerNum)

        dictIn = self.getResponse(playerNum)
        
        # print("client selection: " + dictIn["selection"])

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

        # Sends information to the player about their current hands.
        self.send_players_their_hands()

        # Handle first round of betting.
        self.handle_betting()

        # Checks to see if a player has folded.
        if self.has_folded:
            return

        # Play the flop cards.
        flop_ctr = 0
        remove_card_from_top(deck)
        while flop_ctr < 3:
            card = remove_card_from_top(deck)
            self.table_card_list.append(card)
            flop_ctr += 1

        cards_on_table = self.get_table_list_string()

        # Tells players what cards are on the table.
        self.send_message_all(cards_on_table)

        # Sends information to the player about their current hands.
        self.send_players_their_hands()

        # Handle second round of betting.
        self.handle_betting()

        # Checks to see if a player has folded.
        if self.has_folded:
            return

        # Play the turn card.
        remove_card_from_top(deck)
        turn_card = remove_card_from_top(deck)
        self.table_card_list.append(turn_card)

        cards_on_table = self.get_table_list_string()

        # Tells players what cards are on the table.
        self.send_message_all(cards_on_table)

        # Sends information to the player about their current hands.
        self.send_players_their_hands()

        # Handle third round of betting.
        self.handle_betting()

        # Checks to see if a player has folded.
        if self.has_folded:
            return

        # Play the river card.
        remove_card_from_top(deck)
        river_card = remove_card_from_top(deck)
        self.table_card_list.append(river_card)

        cards_on_table = self.get_table_list_string()

        # Tells players what cards are on the table.
        self.send_message_all(cards_on_table)

        # Sends information to the player about their current hands.
        self.send_players_their_hands()

        # Handle last round of betting.
        self.handle_betting()

    def determine_winner(self):
        """
        Determines the winner and distributes the pot accordingly.
        :return: Updated player statuses
        """
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

        if len(winners) == 2:
            self.send_message_all("You both won! Splitting the pot of size " + str(self.pot) + "evenly \n")
            half_pot = int(self.pot/2)

            for i in range(self.num_players):
                player = self.get_player_from_id(i)

                player.receive_winnings(half_pot)
        else:
            winner = winners[0]
            winner_id = winner[0]

            self.send_message_all(
                "Player " + str(winner_id + 1) + " has won. They receive pot of size " + str(self.pot) + "\n",
            )

            player = self.get_player_from_id(winner_id)

            player.receive_winnings(self.pot)

        self.reset_player_statuses()
        self.pot = 0
        self.has_folded = False

    def send_players_their_hands(self):
        """
        Sends the player their current hand to be printed to terminal.
        :return:
        """
        for i in range(self.num_players):

            player_info = self.get_player_from_id(i)

            hand = player_info.get_hand()

            hand_str = '\nCards in your hand:\n'

            for card in hand:
                hand_str += card[0] + ' of ' + card[1] + '\n'

            self.send_message(hand_str, i)

    def handle_betting(self):
        """
        players will now bet. During this time,
        players have the opportunity to bet, fold, raise, or call.
        """

        for i in range(self.num_players):
            if not self.has_folded:

                message = "Betting Phase: \n"
                options = ["bet", "fold"]

                player = self.get_player_from_id(i)

                result = self.collectCommand(message, options, i)

                if result["selection"] == "fold":
                    player.fold()
                    self.has_folded = True

                    fold_msg = "You have folded"
                    self.send_message(fold_msg, i)

                elif result["selection"] == "bet":
                    bet_amt = result["amount"]
                    result_tup = player.place_bet(bet_amt)

                    while not result_tup[0]:
                        balance = player.get_earnings()

                        fail_msg = "Your maximum balance is " + str(balance)
                        fail_msg += ", \nplace a bet below this amount"
                        result = self.collectCommand(fail_msg, options, i)
                        bet_amt = result["amount"]
                        result_tup = player.place_bet(bet_amt)

                    # Pot is incremented by bet amount.
                    self.pot += result_tup[1]
                    bet_msg = "You have betted " + str(result_tup[1])
                    bet_msg += "\nyour remaining currency is " + str(player.get_earnings())

                    self.send_message(bet_msg, i)

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
    myServer.determine_winner()

myServer.collectCommand("test game state", ["bet", "fold"], 0)   
time.sleep(5)
myServer.shutDown()
