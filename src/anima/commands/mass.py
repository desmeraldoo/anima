import math


def mass(count: int, lp: int, dr: bool) -> int:
    """Calculate the LP total of a mass of enemies using the rules in Those Who
    Walked Amongst Us, Chapter 4: Alternative Combat Systems. Currently assumes
    that the mass is all of one type of being.

    * count: `int`
            * The number of enemies in the mass.
    * lp: `int`
            * The amount of LP of an individual being in the mass.
    * dr: `bool`
            * Whether or not the mass is made up of Damage Resistant beings.
    """
    if dr:
        base_lp = max(int(math.floor(lp / 100.0)) * 100, 100)
        fixed_lp = base_lp // 2
        if count > 50:
            result = base_lp + fixed_lp * 49
            if lp > 1000:
                result += 250 * (count - 50)
            else:
                result += 100 * (count - 50)
        else:
            result = base_lp + (fixed_lp * (count - 1))
    else:
        if count > 100:
            result = max(int(math.floor(lp / 50.0)) * 50, 50) * 100
            if lp > 250:
                result += 25 * (count - 100)
            else:
                result += 10 * (count - 100)
        else:
            result = max(int(math.floor(lp / 50.0)) * 50, 50) * count
    return result
