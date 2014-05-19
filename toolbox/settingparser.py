# coding=utf-8

import configparser
import requests
import shelve
from bs4 import BeautifulSoup
import logging
from base.datatypes import Ressources
import os
from toolbox.tools import colorprint


class SettingsParser(object):
    """
    Get's static things like building costs or unit costs and saves them
    in a shelve file.
    """

    def __init__(self):
        # Create a logger
        self.logger = logging.getLogger('main.SettingParser')
        self.logger.info('creating an instance of SettingGen')

        #specify the path, where the shelve.db file gets stored
        self.config = configparser.ConfigParser()
        self.config.read('settings/settings.ini')
        self.buildingtranslater = {'Hauptgebäude': 'main', 'Stall': 'stable', 'Kaserne': 'barracks',
                                   'Werkstatt': 'garage', 'Schmiede': 'smith',
                                   'Versammlungsplatz': 'place', 'Marktplatz': 'market', 'Bauernhof': 'farm',
                                   'Speicher': 'storage',
                                   'Versteck': 'hide', 'Wall': 'wall', 'Holzfäller': 'wood', 'Lehmgrube': 'stone',
                                   'Eisenmine': 'iron', 'Statue': 'statue', 'Adelshof': 'noble'}
        self.unittranslater = {'Speerträger': 'spear', 'Schwertkämpfer': 'sword', 'Axtkämpfer': 'axe',
                               'Bogenschütze': 'archer',
                               'Späher': 'spy', 'Leichte Kavallerie': 'light', 'Berittener Bogenschütze': 'marcher',
                               'Schwere Kavallerie': 'heavy', 'Rammbock': 'ram', 'Katapult': 'catapult',
                               'Paladin': 'knight',
                               'Adelsgeschlecht': 'snob'}

        # pathfinder
        self.storagepath = self.config.get('storage', 'path')
        self.buildingpath = self.storagepath + os.path.sep +'buildingcost.db'
        self.unitpath = self.storagepath + os.path.sep + 'unitcost.db'

    def buildings_already_stored(self):
        """
        Checks if a valid database already exists.
        """
        if not os.path.exists(os.path.dirname(self.buildingpath)):
            self.logger.info("Dir "+self.buildingpath+" did not exist. Created it.")
            os.mkdir(os.path.dirname(self.buildingpath))

        shelf = shelve.open(self.buildingpath)

        for element in self.buildingtranslater:
            if self.buildingtranslater[element] not in shelf:
                return 0
        return 1

    def units_already_stored(self):
        """
        Checks if a valid unit database already exists.
        """
        shelf = shelve.open(self.unitpath)
        for element in self.unittranslater.values():
            if element not in shelf:
                return 0
        return 1

    def buildings_cost(self):
        """
        This function is used to read the cost of each building from the 'help.die-staemme.de' page.
        It writes all the costs as a dictionairy with 3 parameter per level in a shelve-object called 'shelf'.
        """

        # Return if buildings are already stored
        if self.buildings_already_stored():
            self.logger.info('Buildings are already stored')
            return

        #the url + building[i] is the address where this functions gets the buildingscosts
        url = 'http://help.die-staemme.de/wiki/'

        #initialise shelve
        shelf = shelve.open(self.buildingpath, writeback=True)

        colorprint("[-] Buildingscost not found.", "red")
        #get the required resources for every building in our list
        for element in self.buildingtranslater.keys():

            # initialize new dict & fetch the page
            shelf[self.buildingtranslater[element]] = dict()
            html = requests.get(url + element).text

            # Get the table of all levels
            soup = BeautifulSoup(html)
            table = soup.find_all('table')[-1]

            # comes in, if premium features - which we ignore - are existent.
            # (only for 'Holzfäller', 'Lehmgrube' und 'Eisenmine')
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
                wood = int(splitrow[1].get_text(strip=True).replace('.', ''))
                stone = int(splitrow[2].get_text(strip=True).replace('.', ''))
                iron = int(splitrow[3].get_text(strip=True).replace('.', ''))

                #create a dictionary with the required resources
                dic = {'wood': wood, 'stone': stone, 'iron': iron}

                #write this dict in our shelve
                shelf[self.buildingtranslater[element]][level] = dic
                shelf.sync()

        colorprint("[+] Buildingscost fetched and stored succesfully.", "green")
        shelf.close()

    def unit_cost(self):
        """
        Get _all_ the unitprices!!!
        """

        if self.units_already_stored():
            self.logger.info('units already stored')
            return

        colorprint("[-] Unitcost not found.", "red")
        # Get html
        url = 'http://help.die-staemme.de/wiki/Einheitenübersicht'
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        table = soup.find('table')

        shelf = shelve.open(self.unitpath, writeback=True)

        # The first row is description, the last row
        # is militia (which is free anyway)
        rows = table.find_all('tr')[1:-1]

        for row in rows:
            splitrow = row.find_all('td')
            unitname = splitrow[0].get_text(strip=True)

            wood = int(splitrow[1].get_text(strip=True).replace('.', ''))
            stone = int(splitrow[2].get_text(strip=True).replace('.', ''))
            iron = int(splitrow[3].get_text(strip=True).replace('.', ''))
            pop = int(splitrow[4].get_text(strip=True).replace('.', ''))

            # store fetched data
            shelf[self.unittranslater[unitname]] = {'wood': wood, 'stone': stone, 'iron': iron, 'pop': pop}
        colorprint("[+] Unitcost fetched and stored succesfully.", "green")


def get_buildingprice(building, level):
    level, building = int(level), str(building)
    config = configparser.ConfigParser()
    config.read('settings/settings.ini')
    storagepath = config.get('storage', 'path') + os.path + 'buildingcost.db'
    shelf = shelve.open(storagepath)
    # TODO add not built buildings with lvl 0?

    answer = shelf[building][level]
    return Ressources(wood=answer['wood'], stone=answer['stone'], iron=answer['iron'])

