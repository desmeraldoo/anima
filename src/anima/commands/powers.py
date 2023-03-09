import random
from typing import Final

POWERS: Final[list[str]] = [
    "Fatigue Resistance",
    "Acute Senses",
    "Attribute Increased",
    "Unnatural Size",
    "Inhumanity/Zen",
    "Aquatic Breathing",
    "Reduced Physical Needs",
    "Natural Immunity to an Element",
    "Psychological Immunity",
    "Natural Weapons",
    "Additional Attacks",
    "Increased Damage",
    "Increased Reaction",
    "Damage Energy",
    "Armor Modifier",
    "Special Attack",
    "Poisoned Attack",
    "Added Mystical Effect",
    "Increased Critical",
    "Special Trapping",
    "Supernatural Attack",
    "Elemental Attack",
    "Special Movement",
    "Automatic Transport",
    "Increased Movement",
    "Natural Flight",
    "Mystical Flight",
    "Increased Physical Resistance",
    "Mystical/Psychic Resistance",
    "Regeneration",
    "Physical Immunity",
    "Magical Immunity",
    "Matrix Immunity",
    "Damage Barrier",
    "Physical Armor",
    "Mystical Armor",
    "Innate Magic",
    "Innate Psychic Abilities",
    "Metamorphosis",
    "Invisibility / Undetectable",
    "Aura",
    "Special Means of Vision",
    "Supernatural Detection",
    "Independent Attack",
    "Delayed Attack",
    "Camouflaged Attack",
    "Maintained Attack",
    "Reflect Attacks",
    "Unstoppable",
    "Ranged Natural Weapon",
    "Impact",
    "Conditional Automatic Attack",
    "Breakage Bonus",
    "Automatic Critical",
    "Accumulation Attack",
    "Variable Additional Attacks",
    "Natural Charger",
    "Damage Reduction",
    "Defensive Style",
    "Shield",
    "Improved Special Attack",
    "Special Senses",
    "Gliding",
    "Permanent Effect",
    "Transformation / Evolution",
    "Master of the Supernatural",
]


def powers(count: int = 5) -> str:
    """Returns the names of some randomly-selected monster powers.

    Does not include Divine Powers (those from Those Who WAlked Amongst Us, Chatper 3: Abilities and Powers, Divine Powers) or those that closely resemble such powers (Natural Magic and Systematic Mind).

    * count: `int`
            * The number of powers to select.
    """
    return "POWERS:\n" + "\n".join(random.sample(POWERS, count))
