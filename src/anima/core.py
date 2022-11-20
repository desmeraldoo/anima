import cmd
import itertools
import math
import random
import traceback
from bdb import BdbQuit
from dataclasses import dataclass, field
from importlib.metadata import version
from typing import Final

from tabulate import tabulate

from anima.const import POWERS

ABSORPTION: Final[int] = 30
DUPLICATE_MARKER: Final[str] = "."


@dataclass
class AttackResolver:
    """Stores information related to a single attack-defense exchange in Anima:
    Beyond Fantasy.

    Order matters in this dataclass for how the columns are organized in
    the output table for combo. Upgrading data storage to pandas will
    likely fix this.
    """

    _id: int
    attack: int
    defense: int
    armor: int

    base_damage: int | None = None

    result: str = field(init=False)
    damage: float = field(init=False)

    def __post_init__(self) -> None:
        self.result = calc_attack(
            self.attack, self.defense, self.armor, self.base_damage
        )
        if "ATTACK" or "DAMAGE" in self.result:
            damage_percentage = calc_damage_multiple(
                self.attack - self.defense, self.armor
            )
            if self.base_damage is not None:
                self.damage = damage_percentage * self.base_damage
            else:
                self.damage = damage_percentage
        else:
            self.damage = 0


def parse(args: str) -> tuple[int, ...]:
    """Convert a series of zero or more numbers to an argument tuple."""
    return tuple(map(int, args.split()))


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


def format_extended(lst: list) -> list[int]:
    result = []
    dupe = 0
    for idx in range(len(lst)):
        item = lst[idx]
        if item is None or item == DUPLICATE_MARKER:
            result.append(dupe)
        else:
            dupe = int(item)
            result.append(int(item))
    return result


def calc_combo() -> str:
    """Calculates a combo attack in Anima, which is a combination of various
    attacks, defenses, armor and damage values. By its nature, requires
    additional input from the user.

    Consult the project's documentation for usage examples.
    """

    try:
        atks_input = [_ for _ in input("atks:\t").split(" ") if _ != ""]
        defs_input = [_ for _ in input("defs:\t").split(" ") if _ != ""]
        amrs_input = [_ for _ in input("amrs:\t").split(" ") if _ != ""]
        dmgs_input = [_ for _ in input("dmgs:\t").split(" ") if _ != ""]
    except KeyboardInterrupt:  # Lets the user exit out of the `combo` prompt without exiting the CLI entirely.
        pass

    # Extends each list to be the length of the longest list by filling in later positions with `None`
    atks_extended, defs_extended, amrs_extended, dmgs_extended = map(
        list,
        zip(
            *[
                _
                for _ in itertools.zip_longest(
                    atks_input, defs_input, amrs_input, dmgs_input
                )
            ]
        ),
    )

    atks_formatted = format_extended(atks_extended)
    defs_formatted = format_extended(defs_extended)
    amrs_formatted = format_extended(amrs_extended)
    dmgs_formatted = format_extended(dmgs_extended)

    resolutions = []
    total = 0.0
    for idx, (attack, defense, armor, damage) in enumerate(
        zip(atks_formatted, defs_formatted, amrs_formatted, dmgs_formatted)
    ):
        resolution = AttackResolver(
            _id=idx, attack=attack, defense=defense, armor=armor, base_damage=damage
        )
        resolutions.append(resolution)
        total += resolution.damage
    resolution_headers = [
        "id",
        "attack",
        "defense",
        "armor",
        "base_damage",
        "result",
        "damage",
    ]

    resolution_table = tabulate(
        resolutions, headers=resolution_headers, tablefmt="fancy_grid"  # type: ignore[arg-type] # justification: tabulate supports lists of dataclasses, but mypy doesn't understand this
    )
    total_table = tabulate([[total]], headers=["Total"], tablefmt="fancy_grid")

    return f"\n{resolution_table}\n{total_table}"


def calc_crit(level: int, phr_roll: int, location_id: int = 0) -> str:
    if level > 200:
        level -= (level - 200) // 2
    level -= phr_roll

    if not location_id:
        location_id = random.randint(1, 100)
    location = ""
    if location_id < 11:
        location = "Torso (Ribs)"
    elif location_id < 21:
        location = "Torso (Shoulder)"
    elif location_id < 31:
        location = "Torso (Stomach)"
    elif location_id < 36:
        location = "Torso (Kidneys)"
    elif location_id < 49:
        location = "Torso (Chest)"
    elif location_id < 51:
        location = "Torso (Heart)"
    elif location_id < 55:
        location = "Right arm (Upper forearm)"
    elif location_id < 59:
        location = "Right arm (Lower forearm)"
    elif location_id < 61:
        location = "Right arm (Hand)"
    elif location_id < 65:
        location = "Left arm (Upper forearm)"
    elif location_id < 69:
        location = "Left arm (Lower forearm)"
    elif location_id < 71:
        location = "Left arm (Hand)"
    elif location_id < 75:
        location = "Right leg (Thigh)"
    elif location_id < 79:
        location = "Right leg (Calf)"
    elif location_id < 81:
        location = "Right leg (Foot)"
    elif location_id < 85:
        location = "Left leg (Thigh)"
    elif location_id < 89:
        location = "Left leg (Calf)"
    elif location_id < 91:
        location = "Left leg (Foot)"
    else:
        location = "Head"

    s = f"CRIT LEVEL {level}"
    if level < 1:
        return s + "\n\tNO FURTHER EFFECT"
    elif level < 51:
        return s + f"\n\tMINOR CRITICAL\n\tALL ACTION PENALTY (-{level})"
    else:
        s += f"\n\tMAJOR CRITICAL [{location}]\n\tALL ACTION PENALTY (-{level // 2})\n\tALL ACTION SACRIFICE (-{level // 2})"

        if level > 100:
            if location_id > 90 or (location_id == 49 or location_id == 50):
                s += "\n\tINSTANT DEATH"
            elif location_id > 50 and location_id < 91:
                s += "\n\tAMPUTATION"

            if level > 150:
                s += "\n\tUNCONCIOUS -- AT RISK OF DEATH"

        return s


def chaotic_powers(num_powers: int = 5) -> str:
    return "CHAOTIC POWERS:\n" + "\n".join(random.sample(POWERS, num_powers))


def mass_combat(num: int, lp: int, damage_resistant: int = 0) -> int:
    if damage_resistant:
        base_lp = max(int(math.floor(lp / 100.0)) * 100, 100)
        fixed_lp = base_lp // 2
        if num > 50:
            result = base_lp + fixed_lp * 49
            if lp > 1000:
                result += 250 * (num - 50)
            else:
                result += 100 * (num - 50)
        else:
            result = base_lp + (fixed_lp * (num - 1))
    else:
        if num > 100:
            result = max(int(math.floor(lp / 50.0)) * 50, 50) * 100
            if lp > 250:
                result += 25 * (num - 100)
            else:
                result += 10 * (num - 100)
        else:
            result = max(int(math.floor(lp / 50.0)) * 50, 50) * num
    return result


def shuffle(targets: list[str]) -> str:
    if targets is None or targets == [""]:
        return ""
    s = []
    alt = [_ for _ in targets]
    # The shuffle is only valid if none of the destinations are the same as the starting points.
    while any([x == y for x, y in zip(targets, alt)]):
        random.shuffle(alt)
    for x, y in zip(targets, alt):
        s.append(f"{x} -> {y}")
    return "\n".join(s)


class AnimaShell(cmd.Cmd):
    intro = f"Engaging Anima toolkit (v{version('anima-utils')})"
    prompt = "(anima) "

    def default(self, _: str) -> None:
        print("Input not recognized.")

    def do_atk(self, args: str) -> None:
        "usage: atk attack_roll defense_roll [armor] [base_damage]"
        print(calc_attack(*parse(args)))

    def do_combo(self, _: str) -> None:
        "usage: combo"
        print(calc_combo())

    def do_crit(self, args: str) -> None:
        "usage: crit level phr_roll [location_id]"
        print(calc_crit(*parse(args)))

    def do_chaos(self, args: str) -> None:
        "usage: chaos [num_powers]"
        print(chaotic_powers(*parse(args)))

    def do_mass(self, args: str) -> None:
        "usage: mass [num] [lp] [damage_resistant = 0 | 1]"
        print(mass_combat(*parse(args)))

    def do_shuffle(self, args: str) -> None:
        "usage: shuffle [targets...]"
        print(shuffle(args.split(" ")))

    def do_exit(self, _: str) -> None:
        "terminate session"
        print("Ending session")
        raise KeyboardInterrupt


def main() -> None:
    while True:
        try:
            AnimaShell().cmdloop()
        except (KeyboardInterrupt, BdbQuit):
            raise SystemExit(0)
        except:
            traceback.print_exc()


if __name__ == "__main__":
    main()
