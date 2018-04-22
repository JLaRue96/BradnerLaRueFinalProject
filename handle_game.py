"""
Script used to handle gameplay.
"""

from deck_util import generate_deck
from deck_util import shuffle_deck
from deck_util import remove_card_from_top
from deck_util import add_cards_to_deck
from player import Player
from constants import NUM_POSSIBLE_VALUES
from constants import card_values_dict
from constants import get_val_from_index
from constants import suits
from constants import hand_value_table

import random

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

    TABLE FOR POSSIBLE RETURN VALUES:
    Royal Flush: ('royal flush', 'Ace')
    Straight Flush: ('straight flush', highest value in straight)
    Four of a Kind: ('four of a kind', value of cards in 4ofK)
    Full House: ('full house', value of cards in 3ofK portion of FH)
    Flush: ('flush', high card in flush)
    Straight: ('straight', high card in straight)
    Three of a Kind: ('three of a kind', value of cards in 3ofK)
    Two Pair: ('two pair', value of cards in first pair, value of cards in second pair)
    Pair: ('pair', value of cards in pair)
    High Card: ('nothing', highest value in card list)
    """

    card_list = []
    card_list.append(hand[0])
    card_list.append(hand[1])

    for card in table_list:
        card_list.append(card)

    count_array = generate_count_list(card_list)

    # Check if hand is royal flush
    if has_royal_flush(card_list):
        hand_value = ('royal flush', 'Ace')
    # TODO: STRAIGHT FLUSH
    # Check if hand is four of a kind
    elif has_n_of_same_rank(count_array, 4):
        four_of_kind_rank = get_rank_of_hand(count_array, 4)
        hand_value = ('four of a kind', four_of_kind_rank)
    # Check if hand is full house
    elif has_n_of_same_rank(count_array, 3) and has_n_of_same_rank(count_array, 2):
        full_house_rank = get_rank_of_hand(count_array, 3)
        hand_value = ('full house', full_house_rank)
    # TODO: FLUSH
    # Check if hand is straight
    elif has_straight(count_array):
        straight_rank = get_straight_rank(count_array)
        hand_value = ('straight', straight_rank)
    # Check if hand is three of a kind
    elif has_n_of_same_rank(count_array, 3):
        three_of_kind_rank = get_rank_of_hand(count_array, 3)
        hand_value = ('three of a kind', three_of_kind_rank)
    # Check if hand is a two pair
    elif has_two_pair(count_array):
        two_pair_ranks = get_two_pair(count_array)
        hand_value = ('two pair', two_pair_ranks[0], two_pair_ranks[1])
    # Check if hand is a pair
    elif has_n_of_same_rank(count_array, 2):
        pair_rank = get_rank_of_hand(count_array, 2)
        hand_value = ('pair', pair_rank)
    else:
        high_val = get_high_card(card_list)
        hand_value = ('nothing', high_val)

    return hand_value


def get_rank_of_hand(count_array, n):
    """
    Gets rank of a particular hand.
    --This should only be used for 4oK, 3oK, and pair (NOT two pair)--
    :param count_array: count of instances for each rank.
    :param n: number of instances of rank.
    If n = 2, this function will look for a pair.
    If n = 3, this function will look for a three of a kind.
    If n = 4, this function will look for a four of a kind.
    :return: The rank of the card set in string form. '' if type of hand does
    not exist in card set.
    """

    rank = ''

    for counter, value in enumerate(count_array):
        if value == n:
            rank = get_val_from_index[counter]

    return rank


def get_high_card(card_list):
    """
    Retrieves the highest card value in a list of cards.
    :param card_list: List of cards.
    :return: Highest value in string form.
    """
    high_card = card_list[0]

    for card in card_list:
        if card_values_dict[card[0]] > card_values_dict[high_card[0]]:
            high_card = card

    return high_card[0]


def test_func():
    """
    Simple test function that will generate a random table_list and hand.
    Will determine value of the combination of these two lists.
    :return:
    """
    test_deck = generate_deck()

    ctr = 0

    hand = []

    while ctr < 7:
        index = random.randint(0, len(test_deck) - 1)
        if ctr < 5:
            table_list.append(test_deck[index])
        else:
            hand.append(test_deck[index])
        del test_deck[index]
        ctr += 1

    print("\n\n")
    for card in table_list:
        print(card[0] + " of " + card[1])

    for card in hand:
        print(card[0] + " of " + card[1])

    hand_value = get_hand_value(hand)

    if hand_value[0] == 'two pair':
        print("Hand value: " + hand_value[0] + " of ranks " + hand_value[1] + " and " + hand_value[2])
    else:
        print("Hand value: " + hand_value[0] + " of rank " + hand_value[1])

    print("\n\n")


def has_straight(count_array):
    straight = False
    count = 0

    if len(count_array) != NUM_POSSIBLE_VALUES:
        return straight

    for val in count_array:
        if val > 0:
            count += 1
        else:
            count = 0

        if count == 5:
            straight = True

    return straight


def get_straight_list_indices(count_array):
    straight_count = 0
    start_of_straight_list = -1
    end_of_straight_list = -1

    for counter, value in enumerate(count_array):

        if value > 0:
            start_of_straight_list = counter
            ctr = counter
            while ctr < NUM_POSSIBLE_VALUES:

                if count_array[ctr] > 0:
                    straight_count += 1

                    if straight_count >= 5:
                        end_of_straight_list = ctr

                    ctr += 1

                else:
                    if straight_count < 5:
                        start_of_straight_list = -1

                    break

        if straight_count >= 5:
            break
        else:
            straight_count = 0
            start_of_straight_list = -1

    ind_tup = (start_of_straight_list, end_of_straight_list)

    return ind_tup


def get_straight_rank(count_array):
    straight_indices = get_straight_list_indices(count_array)

    end_index = straight_indices[1]

    rank = get_val_from_index[end_index]

    return rank


def get_two_pair(count_array):
    pair_indices = []

    for counter, value in enumerate(count_array):
        if value == 2:
            pair_indices.append(counter)

    last_index = len(pair_indices) - 1
    second_to_last_index = len(pair_indices) - 2

    rank_one_index = pair_indices[last_index]
    rank_two_index = pair_indices[second_to_last_index]

    rank_one = get_val_from_index[rank_one_index]
    rank_two = get_val_from_index[rank_two_index]

    rank_tup = (rank_one, rank_two)

    return rank_tup


def has_two_pair(count_array):
    count = 0
    two_pair = False

    if len(count_array) != NUM_POSSIBLE_VALUES:
        return two_pair

    for value in count_array:
        if value == 2:
            count += 1

    if count >= 2:
        two_pair = True

    return two_pair


def has_n_of_same_rank(count_array, n):
    """
    Determines if the player has n number of cards with the same value.
    Example input:

    has_n_of_same_rank([0,0,3,0,1,0,1,0,1,0,1,0,0], 3) returns True,
    since the 3rd index has a count of three (i.e. there is a 3 of a kind
    of rank 'Four').

    :param count_array: array that counts rank instances.
    :param n: number that is being searched for in count_array
    :return: True if n exists in array, False if otherwise.
    """
    contains_n_of_same_rank = False

    if len(count_array) != NUM_POSSIBLE_VALUES:
        return contains_n_of_same_rank

    for count in count_array:
        if count == n:
            contains_n_of_same_rank = True

    return contains_n_of_same_rank


def generate_count_list(card_list):
    """
    Takes a list of cards and counts each value instance.
    :param card_list: A list of cards
    :return: An array with each value representing the
    number of instances of a card value mapped to that index.
    """
    card_interpreter_list = [0] * NUM_POSSIBLE_VALUES

    # Builds an array that counts the instance of each card value.
    for card in card_list:
        index = card_values_dict[card[0]]
        card_interpreter_list[index] += 1

    return card_interpreter_list


def has_royal_flush(card_list):
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

    print("High card val = " + get_high_card(rf_card_list))

    print("This should work: " + str(has_royal_flush(rf_card_list)))
    """

    """
    straight_list = [0,1,2,1,1,1,2,1,1,2,2,2,0]

    test = get_two_pair(straight_list)
    """

    test_func()


if __name__ == '__main__':
    main()
