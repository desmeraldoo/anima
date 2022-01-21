# Anima Utilities

Utilities for playing the [Anima: Beyond Fantasy](https://tvtropes.org/pmwiki/pmwiki.php/TabletopGame/AnimaBeyondFantasy) tabletop game. This is a command line utility, and you'll need at least Python to run it.

Note that these calculations use the rules from the original Core rulebook, not Core Exxet. I may add support for Core Exxet in the future if I so choose.

Please open an issue or contact me personally if you see any problems in the calculations. I have done my best to ensure its accuracy but I make no guarantees.

## Installation Instructions

1. Install [Python](https://www.python.org/) and [Git](https://git-scm.com/) if not already installed.
1. Use Git to [clone the repo](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/cloning-a-repository).
1. Launch a [command prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/) in the repository folder, `anima`.
1. Run `python anima.py`. This will launch the command prompt.

## Usage examples

Below are several examples of using the commands, given examples from the Anima: Beyond Fantasy core book or illustrative examples I created.

Optional arguments for every command must be specified in order. That is to say, for the `attack` command, you cannot specify `base_damage` without also specifying `armor`, even if `armor` is just 0.

### attack

usage: attack attack_roll defense_roll [armor] [base_damage]
* attack_roll: The result of the attacker's offensive roll (the sum of their Attack modifier and 1d100).
* defense_roll: The result of the defender's defensive roll (the sum of their Defense modifier and 1d100).
* armor: The relevant AT, given as an integer
* base_damage: The base damage of the weapon used by the attacker, if known or relevant.

> For example, Celia attacks one of the guards with whom she was earlier locked in combat. Celia now has an Attack Ability of 120, while the guard’s Dodge is only 60. Both of them roll the dice. Celia rolls an 86, which, added to her Ability, gives her a Final Attack of 206. The guard’s dice roll is a 44, and so his Final Defense is 104. As Celia is the attacker, the guard’s Final Defense is subtracted from Celia’s Final Attack (206 – 104). The result used when referencing Table 38 is, therefore, 102.

```
(anima) attack 206 104
ATTACK: 100%
```

> Celia had just made an attack with a favorable margin of 102 against the city guard. Since she is wielding a saber against an enemy wearing hardened leather armor, her opponent uses an AT of 2 against her Cutting attack. Consulting the Combat Table, we see that Celia’s attack produces 80% damage. Since the Final Damage number is 45 (only the saber’s Base Damage in this case, since Celia has a 0 Strength Bonus), the guard suffers only 36 points of damage (80% of 45).

```
(anima) attack 206 104 2 45
DAMAGE: 36
```

### crit

usage: crit level phr_roll [location_id]
* level: The final level of the critical, which is the sum of the damage dealt, any critical modifier, and 1d100 rolled by the attacker.
* phr_roll: The final result of the victim's Physical Resistance roll.
* location_id: A way of specifying the location of the critical, if for example the attacker was targeting a specific region of the body. See Table 48 on Page 90 of the core book to look up locations, or simply ignore the output of the program with respect to location if one has already been chosen.

> Muris has just accosted a shopkeeper who was badgering him about his five-finger discount. The shopkeeper doesn't expect his swift sucker punch, so Muris succeeds in his attack and causes 50 damage. The merchant, having only 90 LP, suffers a critical blow, and two more rolls are required to determine the extent of the damage. Muris rolls 1d100 and adds it to the damage caused, and the merchant makes a Physical Resistance Check, using his PhR score of 30 as a base.
> 
> Muris rolls 70, and the merchant rolls only 13, so this is a dire blow with a critical level of 77. The GM rolls to determine the location of the critical, and their roll yields a 67, or the merchants left hand, which seems to have been badly broken in his failed attempt to block the strike.
> 
> Thus, in addition to the damage he received, the merchant suffers not only a -38 All Action Penalty that diminishes at a rate of 5 points per round for the duration of the encounter, but an additional -38 All Action Penalty that heals at a rate dependent on his Constitution, normally 5 points per day (see the core book, page 53). At the discretion of the GM, he may require further medical attention to heal and regain use of his hand. Though, perhaps he should count himself fortunate in one respect—if Muris's critical roll been just 25 points higher, the hand would have been crushed beyond repair.

```
(anima) crit 120 30
CRIT LEVEL 90
        MAJOR CRITICAL [Left arm (Hand)]
        ALL ACTION PENALTY (-45)
        ALL ACTION SACRIFICE (-45)
```


