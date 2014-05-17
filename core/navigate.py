# coding=utf-8

# in diesem file sind _alle_ klassen / funktionen, die
# direkt auf die DS zugreifen.
# sie dienen als interface zwischen der programmlogik und der webseite an sich

import configparser
import requests
import logging
from json import loads
import datetime
from base.datatypes import *
from toolbox.settingparser import get_buildingprice
from toolbox.tools import colorprint
import json


class Bot(object):
    """
    Accesses the website and provides functionality to operate there.
    """

    # Create a lovely session!
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/17.0 Firefox/17.0'})
    html = 'Not initialized yet. Will be initialized with first self.open call.'

    def __init__(self):
        # Bot.session ist eine session vom requests modul


        self.config = configparser.ConfigParser()
        self.config.read(r'settings\settings.ini')

        # get some settings which we will use everywhere.
        self.world = self.config.get('credentials', 'world')

        # Create a logger
        self.logger = logging.getLogger('main.Bot')
        self.logger.info('Bot initialized.')

        if not self.is_logged_in():
            self.buildings = 'Not initialized yet. Will be initialized with first self.open call.'
            self.gamedat = 'Not initialized yet. Will be initialized with first self.open call.'
            self.csrf = 'Not initialized yet. Will be initialized with first self.open call.'
            self.currentvillage = 'Not initialized yet. Will be initialized with first self.open call.'
            self.ressources = 'Not initialized yet. Will be initialized with first self.open call.'
        else:
            self.open("overview")

        # login (if necessary)
        if self.login():
            print("[+] Logged in.")

    def login(self):
        """
        Basic login functionality.
        Returns 1 if successfull else 0.
        """

        # if we are already logged in, we don't need to login again
        if self.is_logged_in():
            # I dont think we need this, do we?
            #self.open('overview')
            print('[+] Already logged in')
            self.logger.info('Already logged in.')
            return

        print('[-] Not logged in. Initiating login procedure.')
        self.logger.info('Login procedure.')

        # fetch the credentials.
        username = self.config.get('credentials', 'username')
        password = self.config.get('credentials', 'password')

        # login parameter
        data = {'user': username,
                'password': password}

        # login
        Bot.session.post('http://www.die-staemme.de/index.php?action=login&server_%s' % self.world, data=data)

        # move to overview
        self.open('overview')

        return 1 if self.is_logged_in() else 0

    def is_logged_in(self):
        """
        Checks if self.br is currently logged in.
        Returns 1 if is logged in else 0.
        """
        Bot.html = Bot.session.get("http://{s}.die-staemme.de/game.php?screen=overview".format(s=self.world)).text
        return 1 if 'var game_data' in Bot.html else 0

    def open(self, place):
        """
        Opens an url and does some extra work
        """

        # Opens an url and gets the response (= html)
        Bot.html = Bot.session.get("http://{self.world}.die-staemme.de/game.php?screen={place}".format(**locals())).text
        self.gamedat = self.get_var_game_data()

        # Wichtige Variablen
        self.csrf = self.gamedat['csrf']
        self.currentvillage = self.gamedat['village']['buildings']['village']
        self.ressources = Ressources(wood=self.gamedat['village']['wood'],
                                     stone=self.gamedat['village']['stone'],
                                     iron=self.gamedat['village']['iron'])
        self.buildings = VarGameDataHandler(self.gamedat).get_buildings()

    def get_next_building(self):
        """
        Extracts data from 'settings\buildings.txt'
        and sets the variable next_building.
        Returns 'storage' if population close to max_population.
        """
        pop = int(self.gamedat["village"]["pop"])
        pop_max = int(self.gamedat["village"]["pop_max"])

        if int(pop_max) * 0.7 < pop:
            return "farm"


        fileo = open(r'settings\buildings.txt', 'r').readlines()
        for line in fileo:
            line = line.strip().split()
            if line:
                building, lvl = line[0], int(line[1])
                if self.buildings[building] < lvl:
                    return building

        return ''

    @staticmethod
    def get_var_game_data():
        """
        get's sexy schmexy var_game_data
        """

        vg = None
        for line in Bot.html.split('\n'):
            if 'var game_data' in line:
                vg = line.split('=', 1)[1].strip()[:-1]
                break

        try:
            vg = loads(vg)
        except TypeError:
            print('dataminer.var_game_data got no json object. this shouldn\'t happen')
            print('probably implement botprot right here')
            raise TypeError
        return vg

    def construct_building(self, building, level):
        # unfortunately we seem to need this ;(
        self.open('main')

        url = "http://{self.world}.die-staemme.de/game.php?" \
              "village={self.currentvillage}&ajaxaction=upgrade_building&h={self.csrf}" \
              "&type=main&screen=main&id={building}&force=1&destroy=0&source={self.currentvillage}".format(**locals())
        resp = Bot.session.get(url).json()
        if resp['success'] != 'Das Gebäude wurde in Auftrag gegeben.':
            print('Status war: ', resp['success'])
            print('Dies ist ein kritischer Fehler. \n Auslösende url: ', url)
            exit()

        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=resp['date_complete'])
        completed = now+delta
        return completed

    def building_manager(self):
        """constructs buildings"""

        storage = TimedBuildings()
        if len(storage):
            print('[*] '+storage.info()+' is beeing constructed right now. Finished in: '+storage.complete()+".")
            return
        next_building = self.get_next_building()

        level = self.buildings[next_building]+1

        # Get price of next building, with level: currentlevel +1
        price = get_buildingprice(next_building, level)

        # do we have enough to build this shit?
        if self.ressources > price:
            response = self.construct_building(next_building, level)
            colorprint('[*] Started construction of '+next_building+".", "turq")
            storage.add(art=next_building, level=level, completed=response)

    def unit_manager(self):
        """
        Builds units. Gets things done. Is awesome
        """

        u = Unit()
        tb = TimedBuildings()

        def default_build():
            # if nothing is beeing constructed right now, don't build units
            if not len(tb):
                return 0

            build_units = []
            if self.buildings["barracks"] >= 3:
                build_units.append("axe")
            else:
                build_units.append("spear")

            # build that
            for unit in build_units:
                if self.ressources > u.getprice(unit)*3:
                    self.make_units(unit, 3)

                elif self.ressources > u.getprice(unit):
                    self.make_units(unit, 1)

        default_build()

    def make_units(self, unit, quantity):
        """
        Builds units. Returns (0, errorcode) on error; (1, msg) on success; -1 on unexpected behaviour.
        """
        # REQUEST FOR TRAINING 1 SPEAR:
        # http://de105.die-staemme.de/game.php?
        #   village=37374&ajaxaction=train&h=2806&mode=train&screen=barracks&&client_time=1399901564
        # h = %csrf%
        # type: POST
        # data: units[spear] = 1

        # Send buildrequest
        data = {"units[%s]" % unit: quantity}
        response = self.session.post("http://de105.die-staemme.de/game.php?village=37374&ajaxaction=train&"
                                     "h={self.csrf}&mode=train&screen=barracks".format(**locals()), data)
        response = json.loads(response.text)

        # Print stuff & return
        if "error" in response.keys():
            colorprint("Failed building "+unit+" (%s)" % quantity, "red")
            colorprint("[-] Error: "+response["error"], "red")
            return 0, response["error"]
        elif "success" in response.keys():
            colorprint("[+] Started building " + unit + " (%s)" % quantity, "turq")
            return 1, response["msg"]
        else:
            colorprint("Unexpected response in function make units.", "red")
            colorprint("response", "red")
            return -1


class VarGameDataHandler(object):
    """Verarbeitet Daten, die immer zur Verfügung stehen."""

    def __init__(self, vg):
        """vg muss dem var gamedata objekt entsprechen"""
        self.vg = vg

    def get_buildings(self):
        """get's sexy schmexy buildings"""
        buildings = self.vg['village']['buildings']
        buildings = {key: int(buildings[key]) for key in buildings}
        return buildings

