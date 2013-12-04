# coding=utf-8
__author__='sudo'

import requests
from bs4 import BeautifulSoup
from json import loads
import threading
import time

class uberattack(threading.Thread):
    def __init__(self, session):
        threading.Thread.__init__(self)
        self.session = session

    def run(self):
        """
        trying to speed things up a little
        """
        #print 'started fattack'
        payload={'spear': '1', 'x': '724', 'y': '464', 'attack': 'Angreifen'}

        r=self.session.post('http://de100.die-staemme.de/game.php?village=54587&try=confirm&screen=place', data=payload)
        response=r.text
        soup=BeautifulSoup(response)

        payload_ch=soup.find('input', attrs={'type': 'hidden', 'name': 'ch'}).get('value')
        payload_action_id=soup.find('input', attrs={'type': 'hidden', 'name': 'action_id'}).get('value')

        payload={'spear': '1', 'x': '724', 'y': '464', 'attack': 'true', 'ch': str(payload_ch), 'action_id': str(payload_action_id),
                 'attack_name': 'test'}

        vgs=get_var_game_data(response)
        csrf=vgs['csrf']

        self.session.post('http://de100.die-staemme.de/game.php?village=54587&action=command&h={csrf}&screen=place'.format(csrf=csrf),
                     data=payload)


def login():
    """
    log me in bitch!
    """
    meine_threads = list()

    payload = {'user': 'main.py', 'password': '996324f8bd524b326e4f258ad75a7d394f5b9326'}
    session = requests.session()
    session.post('http://www.die-staemme.de/index.php?action=login&server_de100', data=payload, verify=False)

    print('init')
    time.clock()
    for a in range(4):
        thread=uberattack(session)
        meine_threads.append(thread)
        thread.start()
    for t in meine_threads:
        t.join()
    print(time.clock())

    print('finit')


def fattack(session):
    """
    trying to speed things up a little
    """
    #print 'started fattack'
    payload={'spear': '1', 'x': '724', 'y': '464', 'attack': 'Angreifen'}

    r=session.post('http://de100.die-staemme.de/game.php?village=54587&try=confirm&screen=place', data=payload)
    response=r.text
    soup=BeautifulSoup(response)

    payload_ch=soup.find('input', attrs={'type': 'hidden', 'name': 'ch'}).get('value')
    payload_action_id=soup.find('input', attrs={'type': 'hidden', 'name': 'action_id'}).get('value')

    payload={'spear': '1', 'x': '724', 'y': '464', 'attack': 'true', 'ch': str(payload_ch), 'action_id': str(payload_action_id),
             'attack_name': 'test', 'sword': '0'}

    vgs=get_var_game_data(response)
    csrf=vgs['csrf']

    session.post('http://de100.die-staemme.de/game.php?village=54587&action=command&h={csrf}&screen=place'.format(csrf=csrf), data=payload)


def get_var_game_data(html):
    """
    get's sexy schmexy var_game_data
    """

    htmllines=html.split('\n')
    vg=None

    for line in htmllines:
        if 'var game_data' in line:
            # vg is a json object
            vg = line.split('=', 1)[1].strip()[:-1]
            break

    try:
        var_game_settings = loads(vg)
    except TypeError:
        print('dataminer.var_game_data got no json object. this shouldn\'t happen')
        raise TypeError
    return var_game_settings

login()


