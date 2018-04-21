""" Functionalities for generating decks and passing out cards

    Decks are lists in the following format:
    Top of Deck --> [Card 1, Card 2, ... , Card n] <-- Bottom of Deck

    Cards are tuples in the following format:
    (value, suit)
    where both value and suit are strings.

    Hands are in the following format:
    [Card, Card]



 """

import random
from constants import PLAYER_ONE_WIN
from constants import PLAYER_TWO_WIN
from constants import PLAYERS_TIE


suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']

card_types = [
    'Two', 'Three', 'Four', 'Five',
    'Six', 'Seven', 'Eight', 'Nine', 'Ten',
    'Jack', 'Queen', 'King', 'Ace'
]


def generate_deck():
    """
    Generates a deck of cards. Cards are tuples of card types and suits
    :return: a 52-card deck, where each card is in form (str, str)
    """

    global suits
    global card_types

    deck = []

    for number in card_types:
        for suit in suits:
            tuple = (number, suit)
            deck.append(tuple)

    return deck


def shuffle_deck(deck):
    """
    Given a deck, this function shuffles said deck and returns this newly shuffled deck.
    :param deck:
    :return: Newly-shuffled deck.
    """

    shuffled_deck = []

    while len(deck) > 0:

        index = random.randint(0, len(deck) - 1)
        card = deck[index]
        shuffled_deck.append(card)
        del deck[index]

    return shuffled_deck


def add_cards_to_deck(card_list, deck):
    """
    Adds a list of cards to a card deck.
    :param card_list: List of cards to be added.
    :param deck: Deck that receives cards.
    :return: Updated deck with cards.
    """

    for card in card_list:
        deck.append(card)

    return deck


def remove_card_from_top(deck):
    """
    Removes and returns the top card of the deck
    :param deck: Deck that contains a variable number of cards.
    :return: The first card of the deck.
    """

    try:
        card = deck[0]
        del deck[0]
        return card

    except IndexError:
        print('The deck is empty!')


"""
def compare_cards(p1_card, p2_card):
    
    # Compares cards from either player. Returns the comparison value.
    # :param p1_card: Card from player 1
    # :param p2_card: Card from player 2
    # :return: 1 is returned if player 1 wins the hand. 2 is returned if player 2 wins the hand.
    # 3 is returned if the result is a tie.
    

    global card_values_dict

    p1_value = card_values_dict.get(p1_card[0])
    p2_value = card_values_dict.get(p2_card[0])

    if p1_value > p2_value:
        return PLAYER_ONE_WIN
    elif p2_value > p1_value:
        return PLAYER_TWO_WIN
    else:
        return PLAYERS_TIE
"""


def pass_out_cards(deck):
    """
    Passes out cards to the players.
    :param deck:
    :return: A tuple of two decks, with the first deck being
    the set of cards that the first player receives, and
    the second deck being the set of cards that the second player receives.
    """

    player_one_deck = []
    player_two_deck = []

    flag = 1

    while deck:

        if flag:

            player_one_deck.append(deck[0])
            flag = 0

        else:

            player_two_deck.append(deck[0])
            flag = 1

        del deck[0]

    tup = (player_one_deck, player_two_deck)

    return tup


def main():
    """
    Main method. Primarily used for testing at this stage in development.
    :return:
    """

    deck = generate_deck()

    print("length of deck = " +str(len(deck)))

    remove_card_from_top(deck)

    print("length of deck now = " + str(len(deck)))

    deck = shuffle_deck(deck)

    passed_out_decks = pass_out_cards(deck)

    print("length of p1 deck = " + str(len(passed_out_decks[0])))

    for card in passed_out_decks[0]:
        print(card[0] + " of " + card[1])

    print("length of p2 deck = " + str(len(passed_out_decks[1])))

    for card in passed_out_decks[1]:
        print(card[0] + " of " + card[1])


if __name__ == '__main__':
    main()
