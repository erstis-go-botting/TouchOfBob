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
        pass

    def __gt__(self, other):
     """ Coparison with ">"
     (Compares if each Value is larger)
     """
     for value in [self.wood, self.stone, self.iron]:
         pass


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


