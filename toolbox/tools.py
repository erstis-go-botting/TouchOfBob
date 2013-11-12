import math

def distance(dorf1, dorf2):
    """
    Erwartet als Parameter zwei Dörfer und gibt ihre Distanz zurück.
    """
    distance = math.sqrt((dorf1.x-dorf2.x)**2 + (dorf1.y-dorf2.y)**2)
    return distance
