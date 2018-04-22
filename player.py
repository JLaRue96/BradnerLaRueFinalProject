class Player:
    """
    This class is used to store information on the player,
    like the player ID, and amount of earnings.
    """

    def __init__(self, player_id, earnings):
        """
        :param player_id: Unique int value for player.
        :param earnings: Starting number of chips to bet with.
        """

        self.player_id = player_id
        self.earnings = earnings

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