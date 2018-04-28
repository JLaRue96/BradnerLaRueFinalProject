class Player:
    """
    This class is used to store information on the player,
    like the player ID, and amount of earnings.
    """

    def __init__(self, player_id, earnings, hand=None):
        """
        :param player_id: Unique int value for player.
        :param earnings: Starting number of chips to bet with.
        :param hand: current hand of the player.
        When the player is initialized, this should be empty.
        """

        self.player_id = player_id
        self.earnings = earnings
        self.hand = hand

    def get_earnings(self):
        """
        :return: The current number of chips that the player posesses.
        """
        return self.earnings

    def get_id(self):
        """
        :return: The unique integer ID of the player.
        """
        return self.player_id

    def get_hand(self):
        """
        :return: player's current hand.
        """
        return self.hand

    def place_bet(self, bet_amt):
        """
        Player places a bet of a specified amount, if the amount if valid
        :param bet_amt: Amount of the bet.
        :return: (True, bet_amt) if bet_amt <= earnings. (False, -1) if not
        """

        result_tup = (False, -1)

        if bet_amt <= self.earnings:
            self.earnings = self.earnings - bet_amt
            result_tup = (True, bet_amt)

        return result_tup

    def set_hand(self, new_hand):
        """
        Sets the current hand of the player.
        :param new_hand: Two card hand. Should be a list of tuples.
        :return: None
        """
        self.hand = new_hand

    def receive_winnings(self, winnings):
        """
        Receive winnings due to winning a round.
        :param winnings: Integer that represents total round winnings
        """
        self.earnings += winnings
