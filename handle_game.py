"""
Script used to handle gameplay.
"""

from deck_util import generate_deck
from deck_util import shuffle_deck
from deck_util import remove_card_from_top
from deck_util import add_cards_to_deck
from constants import NUM_POSSIBLE_VALUES
from constants import card_values_dict
from constants import get_val_from_index
from constants import suits
from constants import hand_value_table

import random

# Global variable for the list of cards on the table.
# This will be filled out throughout the round.


def compare_hands(player_hand_list):
    """
    Determines which player wins the round. May result in a tie.
    Player hand input: (player_id, hand_value, highest_value_card).
    In the case that the player's hand is a two pair, the input will be the following:
    (player_id, hand_value, highest_pair_rank, next_pair_rank)
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
            elif hand_high_card == curr_high_card and hand_value == 'two pair':
                next_high_card = highest_valued_hand[3]
                next_hand_high_card = hand[3]

                if next_hand_high_card > next_high_card:
                    highest_valued_hand = hand

    winners = []

    for hand in player_hand_list:

        if hand[1] == highest_valued_hand[1] and hand[2] == highest_valued_hand[2]:
            if highest_valued_hand[1] == 'two pair':
                if hand[3] == highest_valued_hand[3]:
                    winners.append(hand)
            else:
                winners.append(hand)

    return winners


def get_hand_value(hand, cards_on_table):
    """
    Gets the value of the current hand
    :param hand: the two cards that a particular player is holding.
    :param cards_on_table: List of cards on the table.
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

    for card in cards_on_table:
        card_list.append(card)

    count_array = generate_count_list(card_list)

    # Check if hand is royal flush
    if has_royal_flush(card_list):
        hand_value = ('royal flush', 'Ace')
    # Check if hand is straight flush
    elif has_straight_flush(card_list):
        straight_flush_rank = get_straight_flush_rank(card_list)
        hand_value = ('straight flush', straight_flush_rank)
    # Check if hand is four of a kind
    elif has_n_of_same_rank(count_array, 4):
        four_of_kind_rank = get_rank_of_hand(count_array, 4)
        hand_value = ('four of a kind', four_of_kind_rank)
    # Check if hand is full house
    elif has_n_of_same_rank(count_array, 3) and has_n_of_same_rank(count_array, 2):
        full_house_rank = get_rank_of_hand(count_array, 3)
        hand_value = ('full house', full_house_rank)
    # Check if hand is flush
    elif has_flush(card_list):
        flush_rank = get_flush_rank(card_list)
        hand_value = ('flush', flush_rank)
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


def test_hand_func():
    """
    Simple test function that will generate a random table_list and hand.
    Will determine value of the combination of these two lists.
    :return:
    """
    test_deck = generate_deck()
    table_list = []

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

    hand_value = get_hand_value(hand, table_list)

    if hand_value[0] == 'two pair':
        print("Hand value: " + hand_value[0] + " of ranks " + hand_value[1] + " and " + hand_value[2])
    else:
        print("Hand value: " + hand_value[0] + " of rank " + hand_value[1])

    print("\n\n")


def test_winner_func():
    """
    Simple test function. Will be removed upon final submission.
    :return:
    """
    test_deck = generate_deck()
    table_list = []

    ctr = 0
    num = 0

    hand_list = []

    # Generates the table list.
    while ctr < 5:
        index = random.randint(0, len(test_deck) - 1)
        table_list.append(test_deck[index])
        del test_deck[index]
        ctr += 1

    # Generates the hands of 5 Players.
    while num < 5:

        cards = []

        # Adds two cards to hand
        index = random.randint(0, len(test_deck) - 1)
        cards.append(test_deck[index])
        del test_deck[index]

        index = random.randint(0, len(test_deck) - 1)
        cards.append(test_deck[index])
        del test_deck[index]

        hand = (num, cards[0], cards[1])

        hand_list.append(hand)

        num += 1

    print("\n CARDS ON TABLE \n")

    for card in table_list:
        print(card[0] + " of " + card[1])

    print("\n")

    prepped_list = []

    for hand in hand_list:
        card_one = hand[1]
        card_two = hand[2]
        print("Hand of player " + str(hand[0]) + ": ")
        print(card_one[0] + " of " + card_one[1] + " and ")
        print(card_two[0] + " of " + card_two[1] + "\n")
        hand_list = [hand[1], hand[2]]
        hand_value = get_hand_value(hand_list, table_list)

        if hand_value[0] == 'two pair':
            prepped_tup = (hand[0], hand_value[0], hand_value[1], hand_value[2])
        else:
            prepped_tup = (hand[0], hand_value[0], hand_value[1])

        prepped_list.append(prepped_tup)

    winners = compare_hands(prepped_list)
    # winning_player = winners[0]

    for player in winners:
        print("Winner is player " + str(player[0]) + " with a " + player[1] +
              " of rank " + player[2] + "! ")

    """
    print("Winner is player " + str(winning_player[0]) + " with a " + winning_player[1] +
          " of rank " + winning_player[2] + "! ")
    """
    print("Size of winner list: " + str(len(winners)))


def get_straight_flush_rank(card_array):
    """
    Gets the maximum rank of the straight flush
    :param card_array: List of cards
    :return: rank of the highest valued card in straight flush, in string form.
    """
    straight_flush_rank = ''

    count_array = generate_count_list(card_array)

    indices = get_straight_list_indices(count_array)

    first_index = indices[0]
    last_index = indices[1]

    while last_index - first_index >= 4:

        for suit in suits:
            card_one = (get_val_from_index[first_index], suit)
            card_two = (get_val_from_index[first_index + 1], suit)
            card_three = (get_val_from_index[first_index + 2], suit)
            card_four = (get_val_from_index[first_index + 3], suit)
            card_five = (get_val_from_index[first_index + 4], suit)

            if card_one in card_array and card_two in card_array and \
                    card_three in card_array and card_four in card_array and \
                    card_five in card_array:
                straight_flush_rank = card_five[0]

        first_index += 1

    return straight_flush_rank


def has_straight_flush(card_array):
    """
    Determines whether or not there is a straight flush in the card list.
    :param card_array: Card list
    :return: True if a straight flush exists, false if otherwise.
    """
    straight_flush = False

    if len(card_array) != 7:
        return straight_flush

    count_array = generate_count_list(card_array)

    indices = get_straight_list_indices(count_array)

    first_index = indices[0]
    last_index = first_index + 4

    while last_index <= indices[1]:
        for suit in suits:
            card_val_one = get_val_from_index[first_index]
            card_one = (card_val_one, suit)

            card_val_two = get_val_from_index[first_index + 1]
            card_two = (card_val_two, suit)

            card_val_three = get_val_from_index[first_index + 2]
            card_three = (card_val_three, suit)

            card_val_four = get_val_from_index[first_index + 3]
            card_four = (card_val_four, suit)

            card_val_five = get_val_from_index[first_index + 4]
            card_five = (card_val_five, suit)

            if card_one in card_array and card_two in card_array \
                    and card_three in card_array and card_four in card_array \
                    and card_five in card_array:
                straight_flush = True

        first_index += 1
        last_index += 1

    return straight_flush


def has_flush(card_array):
    """
    Determines whether or not card list contains a flush
    :param card_array: Card list
    :return: True if flush exists in card list, False if otherwise.
    """
    flush = False
    diamond_ctr = 0
    spade_ctr = 0
    club_ctr = 0
    heart_ctr = 0

    if len(card_array) != 7:
        return flush

    for card in card_array:
        suit = card[1]

        if suit == 'Diamonds':
            diamond_ctr += 1
        elif suit == 'Spades':
            spade_ctr += 1
        elif suit == 'Clubs':
            club_ctr += 1
        else:
            heart_ctr += 1

    if diamond_ctr >= 5 or spade_ctr >= 5 or \
            club_ctr >= 5 or heart_ctr >= 5:
        flush = True

    return flush


def find_flush_suit(card_array):
    """
    Determines the suit of the flush
    (as mentioned before, a flush is where at least 5
     of the 7 cards in a card list share the same suit.)
    :param card_array: Card list
    :return: The suit of the card in String form
    """
    diamond_ctr = 0
    spade_ctr = 0
    club_ctr = 0
    heart_ctr = 0

    for card in card_array:
        suit = card[1]

        if suit == 'Diamonds':
            diamond_ctr += 1
        elif suit == 'Spades':
            spade_ctr += 1
        elif suit == 'Clubs':
            club_ctr += 1
        else:
            heart_ctr += 1

    if diamond_ctr == 5:
        suit = 'Diamonds'
    elif spade_ctr == 5:
        suit = 'Spades'
    elif club_ctr == 5:
        suit = 'Clubs'
    else:
        suit = 'Hearts'

    return suit


def get_flush_rank(card_array):
    """
    Gets the maximum card value from a flush.
    :param card_array: A list of cards
    :return: The highest card value in the flush, in String form.
    """
    suit = find_flush_suit(card_array)

    flush_list = []

    for card in card_array:
        if card[1] == suit:
            flush_list.append(card[0])

    max_rank = flush_list[0]

    for val in flush_list:
        if card_values_dict[val] > card_values_dict[max_rank]:
            max_rank = val

    return max_rank


def has_straight(count_array):
    """
    Determines if a count array (derived from card list) has a straight.
    :param count_array: A count array, derived from a card list.
    :return: True if count array has a straight. False if otherwise.
    """
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
    """
    Gets the starting and stopping indices of a straight.
    The starting index = lowest card value in straight.
    Ending index = highest card value in straight.
    :param count_array: A count array from a card list.
    :return: A tuple where the first element is the starting index,
     and the last element is the ending index.
    """
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
    """
    Gets the maximum card value in a straight.
    :param count_array: A count array.
    :return: The maximum card value in a straight in String form.
    """
    straight_indices = get_straight_list_indices(count_array)

    end_index = straight_indices[1]

    rank = get_val_from_index[end_index]

    return rank


def get_two_pair(count_array):
    """
    Retrieves ranks of each pair in count array.
    :param count_array: The count array that contains two pair.
    :return: tuple with the rank of each pair as its elements.
    Note: The pair with the most significant rank is the first element.
    """
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
    """
    Determines if the given count array has a two pair.
    :param count_array: count array (different from a card list,
     see design doc for details).
    :return: True if two pair exists. False if otherwise.
    """
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

    # global suits

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

    test_winner_func()


if __name__ == '__main__':
    main()
