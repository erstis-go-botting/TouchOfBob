# coding=utf-8

# in diesem file sind _alle_ klassen / funktionen, die
# direkt auf die DS zugreifen.
# sie dienen als interface zwischen der programmlogik und der webseite an sich

import configparser
import requests
import logging
from json import loads
import threading
from bs4 import BeautifulSoup
from base.datatypes import *
from toolbox.settingparser import get_buildingprice
from toolbox import settinggeneration
from toolbox.tools import colorprint
import json
from os import path
import re
import time

class Bot(object):
    """
    Accesses the website and provides functionality to operate there.
    """

    # Create a lovely session!
    session = requests.Session()
    a = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount('http://', a)
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/17.0 Firefox/17.0'})
    html = 'Not initialized yet. Will be initialized with first self.open call.'

    def __init__(self):
        # Bot.session ist eine session vom requests modul

        self.ALL_UNITS = ["axe", "spear", "sword", "archer", "spy", "light", "heavy", "catapult", "ram", "marcher"]
        self.config = configparser.ConfigParser()
        self.config.read(r'settings'+path.sep+'settings.ini')

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

        while 1:
            # login (if necessary)
            if self.login():
                print("[+] Logged in.")
                break
            else:
                colorprint("[-] Failed to login. Trying again.", "red")
                time.sleep(5)


        # Fetch other data multithreaded
        self.research = dict()
        self.units = dict()
        self.villagesettings = dict()
        self.grab_infos()

    def grab_infos(self):
        """
        Fetches various stuff multithreaded.
        """
        threads = []
        coollock = threading.Lock()

        # init self.research
        research = threading.Thread(target=self._initresearch, args=(coollock,))
        research.start()
        threads.append(research)

        # init self.units
        units = threading.Thread(target=self._units, args=(coollock,))
        units.start()
        threads.append(units)

        # init self.village_settings
        village_settings = threading.Thread(target=self._getvillageinfo, args=(coollock,))
        village_settings.start()
        threads.append(village_settings)

        for t in threads:
            t.join()

    def _getvillageinfo(self, coollock):
        """
        Gets villagesettings from settingsfile
        """
        S = settinggeneration.SettingGen()
        S.generate_skeleton_villagesettings(village_id=self.gamedat["village"]["id"],
                                            village_name=self.gamedat["village"]["name"])

        village_settings = "settings" + path.sep + "villagesettings.ini"
        villageconfig = configparser.ConfigParser(allow_no_value=True)
        villageconfig.read(village_settings)
        id_ = str(self.gamedat["village"]["id"])
        self.villagesettings["make_coins"] = villageconfig.get(id_, "make_coins")
        self.villagesettings["do_trade"] = villageconfig.get(id_, "do_trade")
        self.villagesettings["do_construct"] = villageconfig.get(id_, "do_construct")
        self.villagesettings["church"] = villageconfig.get(id_, "church")
        self.villagesettings["do_recruit"] = villageconfig.get(id_, "do_recruit")
        self.villagesettings["do_farm"] = villageconfig.get(id_, "do_farm")
        self.villagesettings["dorftyp"] = villageconfig.get(id_, "dorftyp")


    def _initresearch(self, coollock):
        """
        Fetches and sets self.research.
        Fired up in a seperate thread by self.grab_infos()
        """
        if not self.buildings["smith"]:
            self.research = {"spear": 1, "axe": 0, "sword": 0, "archer": 0, "light": 0, "spy": 0, "marcher": 0,
                             "heavy": 0, "ram": 0, "catapult": 0}

        else:
            with coollock:
                self.open("smith")
                soup = BeautifulSoup(self.html)
            researched = str(soup.find("div", id="tech_list").find_all("table", class_="vis tall")[0])
            for u in self.ALL_UNITS:
                # researchable == 2, researched == 1, not researched == 0
                self.research[u] = 2 if u+"_grey" in researched else 1 if u in researched else 0

    def _units(self, coollock):
        """Fetches and sets self.unitbuildtime.
        Fired up in a seperate thread by self.grab_infos()
        """
        barrackunits = ["axe", "spear", "sword", "archer"]
        stableunits = ["spy", "light", "marcher", "heavy"]
        garageunits = ["ram", "catapult"]

        # barracks
        if not self.buildings["barracks"]:
            for u in barrackunits:
                self.units[u] = {"available": 0, "all": 0}

        else:
            with coollock:
                self.open("barracks")
                soup = BeautifulSoup(self.html)
            relevant_lines =soup.find_all("tr", class_="row_a")
            for line in relevant_lines:
                available, all_ = line.find_all("td", style="text-align: center")[0].text.split("/")
                onclick = line.find("a", class_="unit_link")["onclick"]
                art = re.findall(r"'(.+)'", onclick)[0]
                self.units[art] = {"available": int(available), "all": int(all_)}
            # fill with zero
            for u in barrackunits:
                if u not in self.units:
                    self.units[u] = {"available": 0, "all": 0}

        # stable
        if not self.buildings["stable"]:
            for u in stableunits:
                self.units[u] = {"available": 0, "all": 0}

        else:
            with coollock:
                self.open("stable")
                soup = BeautifulSoup(self.html)
            relevant_lines = soup.find_all("tr", class_="row_a")
            for line in relevant_lines:
                available, all_ = line.find_all("td", style="text-align: center")[0].text.split("/")
                onclick = line.find("a", class_="unit_link")["onclick"]
                art = re.findall(r"'(.+)'", onclick)[0]
                self.units[art] = {"available": int(available), "all": int(all_)}
            # fill with zero
            for u in stableunits:
                if u not in self.units:
                    self.units[u] = {"available": 0, "all": 0}

        # garage
        if not self.buildings["garage"]:
            for u in garageunits:
                self.units[u] = {"available": 0, "all": 0}

        else:
            with coollock:
                self.open("garage")
                soup = BeautifulSoup(self.html)
            relevant_lines = soup.find_all("tr", class_="row_a")
            for line in relevant_lines:
                available, all_ = line.find_all("td", style="text-align: center")[0].text.split("/")
                onclick = line.find("a", class_="unit_link")["onclick"]
                art = re.findall(r"'(.+)'", onclick)[0]
                self.units[art] = {"available": int(available), "all": int(all_)}
            # fill with zero
            for u in garageunits:
                if u not in self.units:
                    self.units[u] = {"available": 0, "all": 0}


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

    @staticmethod
    def timestring_to_int(timestring):
        """
        Takes something like 2:02:36
        and returns 122 (60*2 + 02)
        """
        timestring = str(timestring)
        temp = timestring.split(":")
        if len(temp) != 3:
            print("timestring_to_int got unexpected format. Expected something like: 2:02:36. Got: "+timestring)
            return 0
        return 60*int(temp[0]) + int(temp[1])

    def get_barrack_buildtime(self):
        """
        Opens overview and returns the remaining buildtime of barrack-units
        in minutes.
        """
        if not self.gamedat["player"]["premium"]:
            print("Function get_barrac_buildtime is not implemented for non-premium player.")
            return 0

        self.open("overview")
        # how to get building time efficiently:
        # if: soup.find("div", class_="l_main").find("span", class_="timer"):
        #   print(soup.find("div", class_="l_main").find("span", class_="timer").text)
        soup = BeautifulSoup(self.html)
        if soup.find("div", class_="l_barracks").find("span", class_="timer"):
            timestring = soup.find("div", class_="l_main").find("span", class_="timer").text
            return self.timestring_to_int(timestring)
        else:
            return 0

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


        fileo = open('settings'+path.sep+'buildings.txt', 'r').readlines()
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

            # if the unitloop is long, don't build units either
            if not self.buildings["barracks"] or self.get_barrack_buildtime() > 60:
                return 0
            # TODO implement for stable/garage

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

        def primitive_build():
            """ called if "dorftyp" == "off" and level of stable == 0
            """
            if self.units["spear"]["all"] < 50:
                build_units = ["spear"]
            else:
                build_units = ["axe"]

            for unit in build_units:
                if self.research[unit] != 1:
                    continue

                if self.ressources > u.getprice(unit) * 3:
                    self.make_units(unit, 3)

                elif self.ressources > u.getprice(unit):
                    self.make_units(unit, 1)

        if self.villagesettings["dorftyp"] == "off":
            if not self.buildings["stable"]:
                primitive_build()
        else:
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
            return 0
        elif "success" in response.keys():
            colorprint("[+] Started building " + unit + " (%s)" % quantity, "turq")
            return 1
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

