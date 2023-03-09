import itertools
from dataclasses import dataclass, field
from typing import Final

from tabulate import tabulate

from anima.commands.attack import calc_attack, calc_damage_multiple

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
        if self.result in ["ATTACK", "DAMAGE"]:
            damage_percentage = calc_damage_multiple(
                self.attack - self.defense, self.armor
            )
            if self.base_damage is not None:
                self.damage = damage_percentage * self.base_damage
            else:
                self.damage = damage_percentage
        else:
            self.damage = 0


def _format_extended(lst: list) -> list[int]:
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


def combo() -> str:
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
    except (
        KeyboardInterrupt
    ):  # Lets the user exit out of the `combo` prompt without exiting the CLI entirely.
        return ""

    # Extends each list to be the length of the longest list by filling in later positions with `None`,
    # then converts back to individual lists instead of a `zip_longest` object
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

    atks_formatted = _format_extended(atks_extended)
    defs_formatted = _format_extended(defs_extended)
    amrs_formatted = _format_extended(amrs_extended)
    dmgs_formatted = _format_extended(dmgs_extended)

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
