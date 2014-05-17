# coding=utf-8
__author__ = 'sudo'

import logging
import os
import time
from toolbox.setinggeneration import SettingGen
from toolbox.settingparser import SettingsParser
from core.navigate import Bot
import sys


def create_rootlogger():
    """
    Creating a root logger :)
    """
    # gibt es einen logging Ordner?
    if not os.path.exists('logs/'):
        os.makedirs('logs/')
    # create logger with 'main'
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('logs/debug.log')
    fh.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s |%(levelname)-7s |%(name)-20s: %(message)s', datefmt='%d.%m %H:%M:%S')
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.info('created logger')
    return logger


def startup_check():
    """
    Hier werden alle verschiedene Verzeichnisse & Einstellungen geprüft,
    bevor der eigentliche Bot ausgeführt wird.
    """

    # Sind die Settings in Ordnung?
    mylogger.info('Calling SettingGen().check_general_settings')
    SettingGen().check_general_settings()

    # Get all the price shenanigans
    mylogger.info('Checking if db is ok.')
    sp = SettingsParser()
    sp.buildings_cost()
    sp.unit_cost()


def close_and_sleep():
    """
    A function to end the mainloop. Sleeps and logs stuff.
    """
    mylogger.info('\n' + '*' * 100)

    print()
    for i in range(100):
        print('*' * 1, end="")
        sys.stdout.flush()
        time.sleep(300/100)
    print()


if __name__ == '__main__':
    mylogger = create_rootlogger()
    startup_check()

    while 1:
        myb = Bot()  # TODO move out of loop

        myb.building_manager()
        myb.unit_manager()
        close_and_sleep()


# how to get building time efficiently:
# if: soup.find("div", class_="l_main").find("span", class_="timer"):
#   print(soup.find("div", class_="l_main").find("span", class_="timer").text)