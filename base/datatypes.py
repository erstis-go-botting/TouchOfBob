# coding=utf-8
# Put custom datatypes in here!


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