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
from constants import suits

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

