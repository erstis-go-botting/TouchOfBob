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
    It writes all the costs as a dictionairy with 3 parameter per level in a shelve-object called 'shelf'.
    If the
    """
    spec = {'Adelshof': 'Adelshof', 'Statue': 'Statue', 'Kirche': 'Kirche'}

    #the url + urlsnormal[i] is the address where this functions gets the buildingscosts
    url = 'http://help.die-staemme.de/wiki/'
    urlsnormal = ['Hauptgebäude', 'Kaserne', 'Stall', 'Werkstatt','Schmiede', 'Versammlungsplatz', 'Marktplatz',
                  'Bauernhof', 'Speicher', 'Versteck', 'Wall', 'Holzfäller', 'Lehmgrube', 'Eisenmine', 'Statue']

    print urlsnormal
    #print urlsprem

    #specify the path, where the shelve.db file gets stored
    config = ConfigParser.ConfigParser()
    config.read('settings/settings.ini')
    path = config.get('storage', 'path') + '\\buildingcost.db'
    print path

    #emulating a browser
    br = mechanize.Browser()

    #initialise shelve
    shelf = shelve.open(path, writeback=True)

    #get the required resources for every building in our list
    for e in urlsnormal:

        shelf[e] = dict()

        html = br.open(url + e).read()
        # Get the table of all levels
        soup = BeautifulSoup(html)
        table = soup.find_all('table')[-1]

        #comes in, if premium features are possible. (only for 'Holzfäller', 'Lehmgrube' und 'Eisenmine')
        if 'Coinbag' in html:
            rows = table.find_all('tr')[2:]
        else:
            rows = table.find_all('tr')[1:]

        #get the row with all required resources per level
        for row in rows:
            #have a look only on special cells
            splitrow = row.find_all('td')

            #get level, wood, stone and iron separate for each level
            level = int(splitrow[0].get_text(strip=True))
            wood = int(splitrow[1].get_text(strip=True).replace('.',''))
            stone = int(splitrow[2].get_text(strip=True).replace('.',''))
            iron = int(splitrow[3].get_text(strip=True).replace('.',''))

            #create a dictionary with the required resources
            dic = {'wood': wood, 'stone': stone, 'iron': iron}

            #write this dict in our shelve
            shelf[e][level] = dic
            shelf.sync()

            print shelf[e][level]
    #don't waste ram. close our shelve
    shelf.close()



