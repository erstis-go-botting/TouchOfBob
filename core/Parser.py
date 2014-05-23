"""
Various Classes used for parsing stuff.
Most notably a mapparser.
14.05.2014
"""

__author__ = 'zen'
from json import loads
from math import sqrt
import sys


class PrefechParser(object):
    """ Expects a TWMap.sectorPrefech string as input. Returns
    a nicely parsed object.
    """
    # TODO remove self
    parsed_map = dict()

    def __init__(self):

        # TODO replace with actual coordinates
        self.own_coordinates = {"x": 100, "y": 100}




    def analyze_and_add_to_map(self, mapjson):
        """
        Does the whole work!
        """
        try:
            self.mapjson = loads(str(mapjson).split(' = ', 1)[1][:-1])
        except IndexError:
            self.mapjson = loads(str(mapjson))

        parsed_map = dict()

        for superlist in self.mapjson:

            base_x, base_y = superlist['data']['x'], superlist['data']['y']
            sublist = superlist['data']['villages']

            # some of those sublists are dictionaries, some of them are lists.
            # we need them to be of the same format for proper parsing
            # y u do this, ds?

            temp_equal = dict()
            if type(sublist) is dict:
                temp_equal = sublist
            elif type(sublist) is list:
                for i, element in enumerate(sublist):
                    temp_equal[str(i)] = element
            else:
                print('Unexpected type encountered in analyze_map')
                sys.exit(1)

            sublist = temp_equal
            del temp_equal

            for x_modifier in sublist:
                for y_modifier in sublist[x_modifier]:
                    self._analyze_helper(x_modifier, y_modifier, sublist, base_x, base_y, superlist)

    def _analyze_helper(self, x_modifier, y_modifier, sublist, base_x, base_y, superlist):
        """A helper function
        """

        try:
            village = sublist[x_modifier][y_modifier]
        except TypeError:
            print(x_modifier, y_modifier)
            return

            # village is in the form: [u'69473', 7, u'Kentucky', u'342', u'9641899', u'100']
            # a barbarian village is: [u'68444', 4, 0, u'47', u'0', u'100']
            # [0] = villageid, [1] = ?, [2] = village_name, [3] = village_points, [4] = player_id, [5] = ?

            # accessing the account owner: superlist['data']['players'][player_id]
            # which looks like: [u'K\xf6nig Grauer Wolf', u'67', u'839', 0]
            # [0] = name, [1] = points, [2] = alliance_id, [3] = 0 if no noobprot, else string.

        village_id = village[0]
        village_name = village[2]
        if not village_name:
            village_name = 'barbarian village'

        player_id = village[4]
        village_x = int(x_modifier) + int(base_x)
        village_y = int(y_modifier) + int(base_y)

        if player_id == '0':
            player_points = village[3]
            noobprot = 0
            barbarian = 1
        else:
            barbarian = 0
            try:
                player_points = superlist['data']['players'][player_id][1]
                noobprot = superlist['data']['players'][player_id][3]
            except KeyError:
                # verlassenes dorf
                player_points = village[3]
                noobprot = 0

        if noobprot:
            # 1 is more usefull than a string, which we would need to parse for time
            noobprot = 1



        else:
            player_points = player_points.replace('.', '')
            distance = self.distance(self.own_coordinates, {'x': village_x, 'y': village_y})

            # Don't include self :P
            if distance == 0.0:
                self.own_village = {'x': village_x, 'y': village_y, 'player_id': player_id,
                                    'points': int(player_points.replace('.', '')), 'noobprot': noobprot,
                                    'barb': barbarian, 'distance': distance, 'village_id': village_id,
                                    'village_name': village_name,
                                    'village_points': int(village[3].replace('.', ''))}

            self.parsed_map[village_id] = {'x': village_x, 'y': village_y, 'player_id': player_id,
                                      'points': int(player_points.replace('.', '')), 'noobprot': noobprot,
                                      'barb': barbarian, 'distance': distance,
                                      'village_id': village_id, 'village_name': village_name}




    @staticmethod
    def distance(home, target):
        value = (int(home['x']) - int(target['x'])) ** 2 + (int(home['y']) - int(target['y'])) ** 2
        return sqrt(value)


if __name__ == "__main__":
    prefech = open("sectorprefech").read()
    p = PrefechParser(prefech)
