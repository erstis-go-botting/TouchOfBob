# coding=utf-8
__author__='sudo'

import logging
import os
from toolbox.setinggeneration import SettingGen

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
    logger.info('Calling SettingGen().check_general_settings')
    SettingGen().check_general_settings()

logger = create_rootlogger()

startup_check()
