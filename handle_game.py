"""
Script used to handle gameplay.
"""

from deck_util import generate_deck
from deck_util import shuffle_deck
from deck_util import remove_card_from_top
from deck_util import add_cards_to_deck
from player import Player

# Global dictionary used to determine value of hand.
hand_value_table = {

    'nothing': 0, 'pair': 1, 'two pair': 2, 'three of a kind': 3, 'straight': 4,
    'flush': 5, 'full house': 6, 'four of a kind': 7, 'straight flush': 8,
    'royal flush': 9,

}

# global dictionary that evaluates card values.
card_values_dict = {
    'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
    'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10,
    'Ace': 11,
}

# global dictionary for card list interpreter.
list_interpreter_dict = {
    'Two': 0, 'Three': 1, 'Four': 2, 'Five': 3, 'Six': 4, 'Seven': 5,
    'Eight': 6, 'Nine': 7, 'Ten': 8, 'Jack': 9, 'Queen': 10, 'King': 11,
    'Ace': 12,
}

# global list containing all possible card suits.
suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']

# Global variable for the list of cards on the table.
table_list = []


def compare_hands(player_hand_list):
    """
    Determines which player wins the round. May result in a tie.
    Player hand input: (player_id, hand_value, highest_value_card).
    :param player_hand_list: List of remaining player's hands remaining in the round.
    :return: A list containing the winning player(s).
    It's a list so that, in the case of a tie, the pot can be split amongst the winners.
    """
    highest_valued_hand = player_hand_list[0]

    # This initial scan will find the highest-valued hand with the highest-valued high card.
    # A high card is the highest-valued card in a set of cards.

    # TODO: Fix this loop so that the value of the hand is considered as well

    for hand in player_hand_list:

        curr_highest_val = hand_value_table[highest_valued_hand[1]]
        hand_value = hand_value_table[hand[1]]

        if hand_value > curr_highest_val:
            highest_valued_hand = hand

        elif hand_value == curr_highest_val:
            curr_high_card = highest_valued_hand[2]
            hand_high_card = hand[2]

            if hand_high_card > curr_high_card:
                highest_valued_hand = hand

    winners = []

    for hand in player_hand_list:

        if hand[1] == highest_valued_hand[1] and hand[2] == highest_valued_hand[2]:
            winners.append(hand)

    return winners


def get_hand_value(hand):
    """
    Gets the value of the current hand
    :param hand: the two cards that a particular player is holding.
    :return: a tuple with relative card info.
    """

    card_list = []
    card_list.append(hand[0])
    card_list.append(hand[1])

    for card in table_list:
        card_list.append(card)

    # TODO: Add functionality to determine which hand the player has.


def interpret_list(card_list):
    card_interpreter_list = [0] * 13

    for card in card_list:
        index = list_interpreter_dict[card[0]]
        card_interpreter_list[index] += 1

    return card_interpreter_list


def is_royal_flush(card_list):
    """
    Determines if the given list of cards contains a royal flush.
    :param card_list:
    :return:
    """

    global suits

    royal_flush = False

    for suit in suits:
        ten = ('Ten', suit)
        jack = ('Jack', suit)
        queen = ('Queen', suit)
        king = ('King', suit)
        ace = ('Ace', suit)

        if ten in card_list and jack in card_list and \
            queen in card_list and king in card_list and \
                ace in card_list:
            royal_flush = True

    return royal_flush


def main():
    """
    Main method. Primarily used for testing at this stage in development.
    :return:
    """
    rf_card_list = [
        ('Ace', 'Spades'), ('Three', 'Diamonds'), ('King', 'Spades'),
        ('Four', 'Hearts'), ('Queen', 'Spades'), ('Jack', 'Spades'),
        ('Ten', 'Spades')
    ]

    nrf_card_list = [
        ('Three', 'Diamonds'), ('Three', 'Hearts'), ('Three', 'Spades'),
        ('Two', 'Hearts'), ('Jack', 'Diamonds'), ('King', 'Spades'),
        ('Five', 'Clubs')
    ]

    print("This should work: " + str(is_royal_flush(rf_card_list)))

    clist = interpret_list(rf_card_list)

    for position in clist:
        print(str(position))


if __name__ == '__main__':
    main()
