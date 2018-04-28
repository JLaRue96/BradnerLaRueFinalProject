import socket
import json

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


def unpack_cmd(data):
    global latest_command
    latest_command = json.loads(data)


def play_round():

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
    while flop_ctr < 3:
        card = remove_card_from_top(deck)
        table_card_list.append(card)
        flop_ctr += 1

    # TODO: Send Clients list of cards. Should be printed to terminal.
    # TODO: Each Client bets. Clients can also fold if need be.

    # Play the turn card.
    turn_card = remove_card_from_top(deck)
    table_card_list.append(turn_card)

    # TODO: Send Clients list of cards. Should be printed to terminal.
    # TODO: Each Client bets. Clients can also fold if need be.

    # Play the river card.
    river_card = remove_card_from_top(deck)
    table_card_list.append(river_card)

    # TODO: Send Clients list of cards. Should be printed to terminal.
    # TODO: Each Client bets. Clients can also fold if need be.

    # Determine the winner(s).

    pass