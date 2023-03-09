from typing import Final

ABSORPTION: Final[int] = 30


def calc_damage_multiple(result: int, armor: int) -> float:
    """NOTE: Assumes result is greater than 0."""
    if result > 29:
        if armor < 2 and result < 50:
            if armor == 0:
                if result < 40:
                    return 0.1
                else:
                    return 0.3
            else:
                if result < 40:
                    return 0.1
                else:
                    return 0.2
        else:
            return round(((result // 10) / 10) - (armor * 0.1), 1)
    else:
        return 0


def calc_attack(
    attack: int, defense: int, armor: int = 0, base_damage: int | None = None
) -> str:
    """Caulcates the results of an attack and defense exchange between two.

    beings following the rules in the original version of Anima: Beyond Fantasy - Core Rulebook.
    """
    result = attack - defense
    if result < 0:
        counterattack_bonus = -result // 10 * 5
        return f"COUNTERATTACK: +{counterattack_bonus} C"

    if result < ABSORPTION:
        return "MISSED"
    elif (damage_multiple := calc_damage_multiple(result, armor)) <= 0:
        return "DEFLECTED"
    elif not base_damage:
        return f"ATTACK: {int(damage_multiple * 100)}%"
    else:
        return f"DAMAGE: {int(round(base_damage * damage_multiple, 0))}"
