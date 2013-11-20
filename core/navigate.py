# coding=utf-8

# in diesem file sind _alle_ klassen / funktionen, die
# direkt auf die DS zugreifen.
# sie dienen als interface zwischen der programmlogik und der webseite an sich

import ConfigParser
import urllib


class Bot(object):
    """
    Accesses the website and provides functionality to operate there.
    """

    def __init__(self, br):
        # br muss ein Browser sein, geliefert vom mechanize Modul.
        self.br = br
        self.html = 'Not initialized yet. Will be initialized with first self.open call.'

        self.config = ConfigParser.ConfigParser()
        self.config.read(r'settings\settings.ini')

        # get some settings which we will use everywhere.
        self.world=self.config.get('credentials', 'world')

    def login(self):
        """
        Basic login functionality.
        Returns 1 if successfull else 0.
        """

        # if we are already logged in, we don't need to login again
        if self.is_logged_in():
            print 'already logged in'
            return 1

        # fetch the credentials.
        username = self.config.get('credentials', 'username')
        password = self.config.get('credentials', 'password')

        # login parameter
        parameters = {'user': username,
                      'password': password}
        data = urllib.urlencode(parameters)

        # login
        self.br.open('http://www.die-staemme.de/index.php?action=login&server_%s' % self.world, data)

        # move to overview
        self.open('overview')

        return 1 if self.is_logged_in() else 0

    def is_logged_in(self):
        """
        Checks if self.br is currently logged in.
        Returns 1 if is logged in else 0.
        """
        return 1 if 'var game_data' in self.html else 0

    def open(self, place):
        """
        Opens an url and does some extra work
        """

        # Opens an url and gets the response (= html)
        self.html = self.br.open("http://{self.world}.die-staemme.de/game.php?screen={place}".format(**locals())).response().read()

