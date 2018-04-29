import socket
import sys
import time
import cPickle as pickle
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
        self.connections = {}
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

        self.reset_player_statuses()

    def reset_player_statuses(self):
        """
        Updates the player statuses so that
        each player is in play mode.
        :return: None
        """
        for player in self.player_list:
            player.reset_is_playing_status()

    def initialize_player(self):
        """
        Initializes a player.
        Updates the player list to handle this.
        """

        # TODO: Update so that players are initialized with more stuff.
        new_player_id = len(self.player_list)

        new_player = Player(new_player_id, initial_earnings, True)

        self.player_list.append(new_player)


myServer = HoldEmServer()
myServer.acceptClients()
# test sending of data here
myServer.collectCommand("test game state", ["bet", "fold"], 0)   
time.sleep(5)
myServer.shutDown()
