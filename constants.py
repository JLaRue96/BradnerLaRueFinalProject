# Constants for deck and socket utilities (socket constants TBD)

# Card Comparison Constants
PLAYER_ONE_WIN = 1
PLAYER_TWO_WIN = 2
PLAYERS_TIE = 3

# General Constants
NUM_POSSIBLE_VALUES = 13

# Global dictionary used to determine value of hand.
hand_value_table = {

    'nothing': 0, 'pair': 1, 'two pair': 2, 'three of a kind': 3, 'straight': 4,
    'flush': 5, 'full house': 6, 'four of a kind': 7, 'straight flush': 8,
    'royal flush': 9,

}

# global dictionary that evaluates card values.
card_values_dict = {
    'Two': 0, 'Three': 1, 'Four': 2, 'Five': 3, 'Six': 4, 'Seven': 5,
    'Eight': 6, 'Nine': 7, 'Ten': 8, 'Jack': 9, 'Queen': 10, 'King': 11,
    'Ace': 12,
}


# global dictionary to get value of card from an array index.
get_val_from_index = {
    0: 'Two', 1: 'Three', 2: 'Four', 3: 'Five', 4: 'Six', 5: 'Seven',
    6: 'Eight', 7: 'Nine', 8: 'Ten', 9: 'Jack', 10: 'Queen', 11: 'King',
    12: 'Ace',
}

# global list containing all possible card suits.
suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']

# Player initialization information.
initial_earnings = 1000
