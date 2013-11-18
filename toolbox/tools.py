# coding=utf-8

# Hier kommen alle Funktionen rein,
# die komplett unabhängig von den
# andern Funktionalitäten des Bots sind.

import math
import mechanize
import shelve
from bs4 import BeautifulSoup
import ConfigParser


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

    guideline:
    red: something went wrong / is bad...
    yellow: trying to fix something.
    green: fixed something.
    blue: important, but of recurring events.
    turq: important, but often recurring events.
    magenta: something special has happened.
    white: everything as usual. not of particular interest.
    """

    colors = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'magenta': 35, 'turq': 36, 'white': 37}
    print "\033[%sm%s\033[0m" % (colors[color], string)

def buildings_cost(AH=1, statue=1, church=1):
    """
    This function is used to read the cost of each building from the 'help.die-staemme.de' page.
    It writes all the costs as a dictionairy with 3 parameter per level in a shelve-object called 'shel'.
    If the
    """
    spec = {'Adelshof': 'Adelshof', 'Statue': 'Statue', 'Kirche': 'Kirche'}
    url = 'http://help.die-staemme.de/wiki/'
    urlsnormal = ['Hauptgebäude', 'Kaserne', 'Stall', 'Werkstatt','Schmiede', 'Versammlungsplatz',
                                   'Marktplatz', 'Bauernhof', 'Speicher', 'Versteck', 'Wall']
    urlsprem = [url + e for e in ['Holzfäller', 'Lehmgrube', 'Eisenmine']]
    print urlsnormal
    print urlsprem

    config = ConfigParser.ConfigParser()
    config.read('settings/settings.ini')
    path = config.get('storage', 'path') + '\\buildingcost.db'
    print path

    br = mechanize.Browser()
    for e in urlsnormal:
        soup = BeautifulSoup(br.open(url + e).read())
        table = soup.find_all('table')[-1]
        rows = table.find_all('tr')[1:]
        for row in rows:
            shel = shelve.open(path)
            splitrow = row.find_all('td')
            #print splitrow
            level = int(splitrow[0].get_text(strip=True))
            wood = int(splitrow[1].get_text(strip=True).replace('.',''))
            stone = int(splitrow[2].get_text(strip=True).replace('.',''))
            iron = int(splitrow[1].get_text(strip=True).replace('.',''))
            dic = {'wood': wood, 'stone': stone, 'iron': iron}
            shel[e][level] = dic
            shel.close()
            shel = shelve.open(path)
            print shel[e][level]




