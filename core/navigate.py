# coding=utf-8

# in diesem file sind _alle_ klassen / funktionen, die
# direkt auf die DS zugreifen.
# sie dienen als interface zwischen der programmlogik und der webseite an sich


class Bot(object):
    """
    Accesses the website and provides functionality to operate there.
    """

    def __init__(self, br):
        # br muss ein Browser sein, geliefert vom mechanize Modul.
        self.br = br

    def login(self):
        """
        Basic login functionality.
        Returns 1 if successfull else 0.
        """
        pass

    def is_logged_in(self):
        """
        Checks if self.br is currently logged in.
        Returns 1 if is logged in else 0.
        """
        pass