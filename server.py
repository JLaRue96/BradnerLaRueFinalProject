import socket
import json

from constants import initial_earnings
from deck_util import generate_deck
from deck_util import shuffle_deck
from deck_util import remove_card_from_top
from handle_game import compare_hands
from handle_game import get_hand_value
from player import Player

latest_command = ""

# Global list of players
# Format: [Player, Player, ...]
player_list = []

# Global list of cards.
# Format: [(Rank, Suit), (Rank, Suit), ...]
table_card_list = []

# Global information regarding how much money is on the table.
pot = 0


def unpack_cmd(data):
    global latest_command
    latest_command = json.loads(data)


def initialize_player():
    """
    Initializes a player.
    Updates the player list to handle this.
    """

    # TODO: Update so that players are initialized with more stuff.
    new_player_id = len(player_list)

    new_player = Player(new_player_id, initial_earnings, True)

    player_list.append(new_player)


def play_round():
    """
    Plays a round of Hold'em.
    Assumes that all players will remain in the game
    for the duration of the round.
    :return:
    """

    global table_card_list

    # Load and shuffle the deck
    deck = shuffle_deck(generate_deck())

    # Reset the table_card_list if it currently
    # contains cards.
    table_card_list = []

    # Gives two cards to each of the players.
    for player in player_list:

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
        table_card_list.append(card)
        flop_ctr += 1

    # TODO: Send Clients list of cards. Should be printed to terminal.
    # TODO: Each Client bets. Clients can also fold if need be.

    # Play the turn card.
    remove_card_from_top(deck)
    turn_card = remove_card_from_top(deck)
    table_card_list.append(turn_card)

    # TODO: Send Clients list of cards. Should be printed to terminal.
    # TODO: Each Client bets. Clients can also fold if need be.

    # Play the river card.
    remove_card_from_top(deck)
    river_card = remove_card_from_top(deck)
    table_card_list.append(river_card)

    # TODO: Send Clients list of cards. Should be printed to terminal.
    # TODO: Each Client bets. Clients can also fold if need be.

    player_info_tuple_list = []

    # Get Player info tuples.
    # Tuple format: (Player ID, Player's hand value, highest rank of Player's hand value)
    for player in player_list:

        if player.has_not_folded():

            hand_value = get_hand_value(player.get_hand(), table_card_list)

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

    reset_player_statuses()


def reset_player_statuses():
    """
    Updates the player statuses so that
    each player is in play mode.
    :return: None
    """
    for player in player_list:
        player.reset_is_playing_status()
