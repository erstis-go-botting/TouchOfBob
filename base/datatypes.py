# coding=utf-8
# Put custom datatypes in here!

from configparser import ConfigParser
import datetime
import shelve


class Village(object):
    """
    Eine Klasse um Dörfer zu repräsentieren.
    Bertrand wäre stolz auf uns.

    Usage:

    >>> myv = Village(x=100, y=100, playername='main.py', villagename=u'imba döörf',
    ... villagepoints = 100, playerpoints = 100, villageid = 109894, playerid=83782)
    >>> print myv
    imba döörf from main.py at (100|100) with 100 points.
    >>> myv = Village(x=100, y=100, playername='', villagename='barbarendorf',
    ... villagepoints = 100, playerpoints = 100, villageid = 109894, playerid=0)
    >>> print myv
    Barbarian village at (100|100) with 100 points.
    >>> print type(myv)
    <class 'Village'>

    Parameter:
    x, y, villagepoints, playerpoints, villageid, playerid, villagename, playername
    """
    def __init__(self, x, y, villagepoints, playerpoints, villageid, playerid, villagename='', playername=''):

        self.x = int(x)
        self.y = int(y)
        self.villagepoints = int(villagepoints)
        self.playerpoints = int(playerpoints)
        self.villageid = int(villageid)
        self.playerid = int(playerid)

        self.villagename = villagename.encode('utf-8')
        self.playername = playername.encode('utf-8')

    def __str__(self):
        if self.playerid:
            return '{self.villagename} from {self.playername} at ({self.x}|{self.y}) with {self.villagepoints} points.'.format(**locals())
        else:
            return 'Barbarian village at ({self.x}|{self.y}) with {self.villagepoints} points.'.format(**locals())


class Ressources(object):

    def __init__(self, wood, stone, iron):

        self.wood = int(wood)
        self.stone = int(stone)
        self.iron = int(iron)

    def __str__(self):
        """print(Ressources) --> "Ressources: (a|b|c)"""
        return "Ressources: ({self.wood}|{self.stone}|{self.iron})".format(**locals())

    def __lshift__(self, other):
        """ Comparison "<<" """
        return max([self.wood, self.iron, self.stone]) < int(other)

    def __rshift__(self, other):
        """ Comparison ">>" """
        return max([self.wood, self.iron, self.stone]) > int(other)

    def __lt__(self, other):
        """ Comparison with "<"
        (Compares if each Value is smaller)
        """
        l1 = [self.wood, self.stone, self.iron]
        l2 = [other.wood, other.stone, other.iron]
        for i in range(3):
            if l1[i] > l2[i]:
                return False
        return True

    def __gt__(self, other):
        """ Coparison with ">"
        (Compares if each Value is larger)
        """
        l1 = [self.wood, self.stone, self.iron]
        l2 = [other.wood, other.stone, other.iron]
        for i in range(3):
            if l1[i] < l2[i]:
                return False
        return True



    def __abs__(self):
        """ abs(Ressources) -> integer"""
        return sum([self.wood + self.stone + self.iron])

    def __add__(self, other):
        """ Add two instances of type Ressources to each other"""
        self.wood += other.wood
        self.iron += other.iron
        self.stone += other.stone

    def __sub__(self, other):
        """ Subtract two instances of type Ressources from each other"""
        self.wood -= other.wood
        self.stone -= other.stone
        self.iron -= other.iron

    def __mul__(self, other):
        """ "Multiplies some Value to each ressource"""
        self.wood *= other
        self.stone *= other.stone
        self.iron *= other.iron


class TimedBuildings(object):
    """ Proof of concept stuff.
    Used for logging?
    """

    # TODO implement removal of old entries (eg: datetime.datetime.now() >
    # TODO tb.db["under_construction"][0]['complete'].

    def __init__(self):

        self.config = ConfigParser()
        self.config.read('settings/settings.ini')
        self.storagepath = self.config.get('storage', 'path')
        self.db = shelve.open(self.storagepath + '\\timedbuildings.db', flag="c", writeback=True)

        # clear old elements
        self.delete_old_elements()

    def delete_old_elements(self):
        """
        Deletes elements which are completed.
        """

        # If there are no elements stored, quit with returncode 1
        if "under_construction" not in self.db.keys() or not self.db["under_construction"]:
            return 1

        now = datetime.datetime.now()
        for i, element in enumerate(self.db["under_construction"][:]):
            if element["complete"] < now:
                self.db["under_construction"].remove(element)
        self.db.sync()

    def refresh(self):
        self.db.close()
        self.db = shelve.open(self.storagepath + '\\timedbuildings.db')

    def add(self, art, level, completed):

        key = 'under_construction'
        if key in self.db:
            temp = self.db[key]
            temp.append({'art': art, 'level': level, 'complete': completed})
            self.db[key] = temp
        else:
            self.db[key] = [{'art': art, 'level': level, 'complete': completed}]
        self.refresh()

    def complete(self):
        """
        Returns time in minutes until next building is built.
        """
        if "under_construction" not in self.db.keys() or not self.db["under_construction"]:
            return 0

        timedelta = self.db["under_construction"][0]["complete"] - datetime.datetime.now()
        minutes = int(timedelta.total_seconds() // 60)
        seconds = int(timedelta.seconds) - minutes * 60

        return str(minutes)+"."+str(seconds)

    def info(self):
        """
        Returns type of building + level which is beeing built atm.
        """
        if "under_construction" not in self.db.keys() or not self.db["under_construction"]:
            return 0

        art = self.db["under_construction"][0]["art"]
        level = self.db["under_construction"][0]["level"]
        return str(art)+" "+str(level)


    def __str__(self):
        if 'under_construction' not in self.db:
            return 0
        result = ""
        for element in self.db['under_construction']:
            result = result+str(element)+"\n"
        return result

    def __len__(self):
        if 'under_construction' not in self.db:
            return 0
        else:
            return len(self.db['under_construction'])

    def __del__(self):
        self.db.close()