# coding=utf-8

# Hier kommen alle Funktionen rein,
# die komplett unabhängig von den
# andern Funktionalitäten des Bots sind.

import math
import mechanize


def distance(dorf1, dorf2):
    """
    Erwartet als Parameter zwei Dörfer und gibt ihre Distanz zurück.
    """
    distance = math.sqrt((dorf1.x-dorf2.x)**2 + (dorf1.y-dorf2.y)**2)
    return distance


def create_browser():
    """
    Returns an usefull browser.
    """

    browser = mechanize.Browser( factory = mechanize.RobustFactory( ) )
    browser.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/17.0 Firefox/17.0")]
    browser.set_handle_robots( False )
    return browser


def colorprint(string, color='blue'):
    """
    Prettifies output.
    Makes debugging fun again.

    usage:
    >>> colorprint('test', 'magenta')

    :param string: Just a string you want to have printed.
    :type string: string, obviously
    :param color: the color you want to use.
    :type color: string
    """

    colors = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'magenta': 35, 'turq': 36, 'white': 37}
    print "\033[%sm%s\033[0m" % (colors[color], string)