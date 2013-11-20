# coding=utf-8

import configparser
import requests
import shelve
from bs4 import BeautifulSoup

class SettingsParser(object):

    def buildings_cost(self, AH=1, statue=1, church=1):
        """
        This function is used to read the cost of each building from the 'help.die-staemme.de' page.
        It writes all the costs as a dictionairy with 3 parameter per level in a shelve-object called 'shelf'.
        If the
        """
        spec = {'Adelshof': 'Adelshof', 'Statue': 'Statue', 'Kirche': 'Kirche'}

        #the url + building[i] is the address where this functions gets the buildingscosts
        url = 'http://help.die-staemme.de/wiki/'
        building = ['Hauptgebäude', 'Kaserne', 'Stall', 'Werkstatt','Schmiede', 'Versammlungsplatz', 'Marktplatz',
                    'Bauernhof', 'Speicher', 'Versteck', 'Wall', 'Holzfäller', 'Lehmgrube', 'Eisenmine', 'Statue']


        #specify the path, where the shelve.db file gets stored
        config = configparser.ConfigParser()
        config.read('settings/settings.ini')
        path = config.get('storage', 'path') + '\\buildingcost.db'
        print(path)

        #initialise shelve
        shelf = shelve.open(path, writeback=True)

        #get the required resources for every building in our list
        for element in building:

            # initialize new dict & fetch the page
            shelf[element] = dict()
            html = requests.get(url + element).text

            # Get the table of all levels
            soup = BeautifulSoup(html)
            table = soup.find_all('table')[-1]

            #comes in, if premium features - which we ignore - are existent. (only for 'Holzfäller', 'Lehmgrube' und 'Eisenmine')
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
                shelf[element][level] = dic
                shelf.sync()

                print(shelf[element][level])

        #don't waste ram. close our shelve
        shelf.close()



