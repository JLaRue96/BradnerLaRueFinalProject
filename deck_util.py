""" Functionalities for generating decks and passing out cards """

import random
from constants import PLAYER_ONE_WIN
from constants import PLAYER_TWO_WIN
from constants import PLAYERS_TIE


# global dictionary that evaluates card values.
card_values_dict = {
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
    'Ace': 11,
}

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


def compare_cards(p1_card, p2_card):
    """
    Compares cards from either player. Returns the comparison value.
    :param p1_card: Card from player 1
    :param p2_card: Card from player 2
    :return: 1 is returned if player 1 wins the hand. 2 is returned if player 2 wins the hand.
    3 is returned if the result is a tie.
    """

    global card_values_dict

    p1_value = card_values_dict.get(p1_card[0])
    p2_value = card_values_dict.get(p2_card[0])

    if p1_value > p2_value:
        return PLAYER_ONE_WIN
    elif p2_value > p1_value:
        return PLAYER_TWO_WIN
    else:
        return PLAYERS_TIE


def main():
    """
    Main method. Primarily used for testing at this stage in development.
    :return:
    """

    deck = generate_deck()

    print('ORIGINAL DECK LIST')

    for card in deck:
        print(card[0] + " of " + card[1])

    shuff = shuffle_deck(deck)

    print('SHUFFLED DECK LIST')

    for card in shuff:
        print(card[0] + " of " + card[1])

    card_1 = ('Four', 'Diamonds')
    card_2 = ('King', 'Spades')

    compare_value = compare_cards(card_1, card_2)

    print('Comparison Value: ' + str(compare_value))


if __name__ == '__main__':
    main()
