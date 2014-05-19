# coding=utf-8
""" settinggeneration

In diesem File ist genau eine Klasse, SettingGen, die verschiedene
Funktionen bereitstellt um Settings (d.h. ini files) überprüfen &
erstellen zu können.
"""


import time
import configparser
import os
from toolbox.tools import colorprint
import logging


class SettingGen(object):
    def __init__(self):

        self.logger = logging.getLogger('main.SettingGen')
        self.logger.info('creating an instance of SettingGen')

        if not os.path.exists('settings/'):
            os.makedirs('settings/')
            colorprint('Folder [settings] did not exist. Created it.', 'green')

        self.settingpath = "settings"+os.path.sep+"settings.ini"  # os.path.sep = portability shenanigans
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read(self.settingpath)

    def check_general_settings(self):
        """
        Generates the standard skeleton for settings.ini
        """

        self.generate_description_general_settings()
        if not self.config.has_section('description'):
            colorprint('[description] in [{self.settingpath}] did not exist. Created it.'.format(**locals()), 'green')

        if not self.config.has_section('credentials'):
            self.config.add_section('credentials')
            self.config.set('credentials', 'world', 'de100')
            self.config.set('credentials', 'username', 'yournamegoeshere')
            self.config.set('credentials', 'password', 'yourpasswordgoeshere')
            self.config.set('credentials', 'captcha_user', 'yourdeathbycaptchaussernamegoeshere')
            self.config.set('credentials', 'captcha_pass', 'yourdeathbycaptchapasswordgoeshere')
            colorprint('[credentials] in [{self.settingpath}] did not exist. Created it.'.format(**locals()), 'green')

        if not self.config.has_section('control'):
            self.config.add_section('control')
            self.config.set('control', 'sleep', '300')
            self.config.set('control', 'farmsplit', '5')
            colorprint('[control] in [{self.settingpath}] did not exist. Created it.'.format(**locals()), 'green')

        if not self.config.has_section('storage'):
            self.config.add_section('storage')
            self.config.set('storage', 'path', 'data')
            colorprint('[storage] in [{self.settingpath}] did not exist. Created it.'.format(**locals()), 'green')

        self.config.write(open(self.settingpath, 'w'))

    def generate_skeleton_villagesettings(self, village_id, village_name):
        """
        Generates the standard skeleton for villagesettings.ini
        """

        settingpath=self.config.get('storage', 'worldsettingspath')
        config=configparser.SafeConfigParser(allow_no_value=True)
        config.read(settingpath)

        village_id = str(village_id)

        if config.has_section(village_id):
            print('woah, stop right there, that shit allready exists.')
            return

        config.add_section(village_id)

        config.set(village_id, '# {village_name}'.format(**locals()))
        config.set(village_id, 'make_coins', '0')
        config.set(village_id, 'do_trade', '1')
        config.set(village_id, 'do_recruit', '1')
        config.set(village_id, 'do_farm', '1')
        config.set(village_id, 'do_construct', '1')
        config.set(village_id, 'church', '0')
        config.set(village_id, 'Dorftyp', 'off')

        with open(settingpath, 'w') as cfile:
            config.write(cfile)
            time.sleep(1)

    def generate_description(self, path):
        """
        a function to a add a little bit of
        description to villagesettings.ini
        """

        self.config.add_section('description')

        self.config.set('description', '# Hier können individuelle Einstellungen zu einzelnen Dörfern gesetzt werden.')
        self.config.set('description', '# Die Settings in settings/settings.ini/control sind immernoch relevant.')
        self.config.set('description', '# Diese werden quasi als globale Settings verwendet.')

        with open(path, 'w') as cfile:
            self.config.write(cfile)

    def generate_description_general_settings(self):
        """
        a function to a add a little bit of
        description to settings.ini
        """

        if not self.config.has_section('description'):
            self.config.add_section('description')

        self.config.set('description', '# Ein generelles Settingfile.')
        self.config.set('description', '# Hier werden statische Daten gespeichert, die von user zu user')
        self.config.set('description', '# und von Welt zu Welt verschieden sind. Diese Daten hier können')
        self.config.set('description', '# nicht automatisch generiert werden.')

        with open(self.settingpath, 'w') as cfile:
            self.config.write(cfile)



