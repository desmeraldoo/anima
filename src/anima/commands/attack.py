import math


def calc_damage_multiple(result: int, armor: int) -> float:
    """NOTE: Assumes result is greater than 0."""
    if result > 0:
        return (result / 100) - (armor * 0.1)
    else:
        return 0


def calc_attack(
    attack: int, defense: int, armor: int = 0, base_damage: int | None = None
) -> str:
    """Caulcates the results of an attack and defense exchange between two.

    beings following the rules in the original version of Anima: Beyond Fantasy - Core Rulebook.
    """
    result = attack - defense
    if result <= 0:
        counterattack_bonus = -result // 10 * 5
        return f"COUNTERATTACK: +{counterattack_bonus} C"

    elif (damage_multiple := calc_damage_multiple(result, armor)) <= 0:
        return "DEFLECTED"
    elif not base_damage:
        return f"ATTACK: {int(damage_multiple * 100)}%"
    else:
        return f"DAMAGE: {math.ceil(base_damage * damage_multiple)}"
