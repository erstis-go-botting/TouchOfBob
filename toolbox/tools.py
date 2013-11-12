def laufzeit(dorf1, dorf2, einheitentyp):
    if einheitentyp == "lkav":
        mod = 10
    else:
        mod = 20
    return math.sqrt((dorf1.x-dorf2.x)**2 + (dorf1.y-dorf2.y)**2)*mod
