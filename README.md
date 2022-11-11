# Anima Utilities

Command line utilities for playing the [Anima: Beyond Fantasy](https://tvtropes.org/pmwiki/pmwiki.php/TabletopGame/AnimaBeyondFantasy) tabletop game.

Note that these calculations are not guaranteed to be from either the Core rulebook or the updated version, Core Exxet. I believe that I'm using the damage formula from Core Exxet. If you see a problem, [open an issue](https://github.com/desmeraldoo/anima/issues/new).

## Installation

### From Pypi

1. Install [Python](https://www.python.org/) and [Git](https://git-scm.com/) if not already installed.
1. Run `pip install anima` to install the program.
1. Run `anima` to open the command prompt.

### From Source

1. Use Git to [clone the repo](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/cloning-a-repository).
1. Launch a [command prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/) in the repository folder, `anima`.
1. Run `python install .`, which will build and install the package and add the `anima` command to your system.
1. Run `anima` to open the command prompt.

If you have any problems following the steps above, [open an issue](https://github.com/desmeraldoo/anima/issues/new).

## Documentation

The below demonstrations of how to use the commands use examples from the *Anima: Beyond Fantasy* core book or original illustrative examples.

### atk

Resolves an attack and defense exchange.

`usage: atk attack_roll defense_roll armor_value base_damage`

| field        | type | default | description                                                               |
| ------------ | ---- | ------- | ------------------------------------------------------------------------- |
| attack_roll  | int  | 0       | The final result of the attacker's offensive roll.                        |
| defense_roll | int  | 0       | The final result of the defender's defensive roll.                        |
| attack_roll  | int  | 0       | The defender's Armor on the Table corresponding to the attacker's attack. |
| attack_roll  | int  | 0       | The base damage of the weapon used by the attacker, if known or relevant. |

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

### combo

Enters a special interactive mode where the user can specify multiple attacks and resolve them all at once.

There is no need to enter the total number of attacks up front. The longest list is taken as the true number of attacks. Blanks are replaced with zero, and `'.'` values are replaced with the closest preceding non-null value, or zero, in the absence of any such value.

`usage: combo`

```
(anima) combo
atks:   150 180 170 210
defs:   160 120 200 130
amrs:   2 4 6 8
dmgs:   100 80 60 40

╒══════╤══════════╤═══════════╤═════════╤═══════════════╤══════════════════════╤══════════╕
│   id │   attack │   defense │   armor │   base_damage │ result               │   damage │
╞══════╪══════════╪═══════════╪═════════╪═══════════════╪══════════════════════╪══════════╡
│    0 │      150 │       160 │       2 │           100 │ COUNTERATTACK: +5 C  │        0 │
├──────┼──────────┼───────────┼─────────┼───────────────┼──────────────────────┼──────────┤
│    1 │      180 │       120 │       4 │            80 │ DAMAGE: 16           │       16 │
├──────┼──────────┼───────────┼─────────┼───────────────┼──────────────────────┼──────────┤
│    2 │      170 │       200 │       6 │            60 │ COUNTERATTACK: +15 C │        0 │
├──────┼──────────┼───────────┼─────────┼───────────────┼──────────────────────┼──────────┤
│    3 │      210 │       130 │       8 │            40 │ MISSED               │        0 │
╘══════╧══════════╧═══════════╧═════════╧═══════════════╧══════════════════════╧══════════╛
╒═════════╕
│   Total │
╞═════════╡
│      16 │
╘═════════╛
```

```
(anima) combo
atks:   150 160 170 180
defs:
amrs:   10
dmgs:   50 . . 150

╒══════╤══════════╤═══════════╤═════════╤═══════════════╤═════════════╤══════════╕
│   id │   attack │   defense │   armor │   base_damage │ result      │   damage │
╞══════╪══════════╪═══════════╪═════════╪═══════════════╪═════════════╪══════════╡
│    0 │      150 │         0 │      10 │            50 │ DAMAGE: 25  │       25 │
├──────┼──────────┼───────────┼─────────┼───────────────┼─────────────┼──────────┤
│    1 │      160 │         0 │      10 │            50 │ DAMAGE: 30  │       30 │
├──────┼──────────┼───────────┼─────────┼───────────────┼─────────────┼──────────┤
│    2 │      170 │         0 │      10 │            50 │ DAMAGE: 35  │       35 │
├──────┼──────────┼───────────┼─────────┼───────────────┼─────────────┼──────────┤
│    3 │      180 │         0 │      10 │           150 │ DAMAGE: 120 │      120 │
╘══════╧══════════╧═══════════╧═════════╧═══════════════╧═════════════╧══════════╛
╒═════════╕
│   Total │
╞═════════╡
│     210 │
╘═════════╛
```

```
(anima) combo
atks:   280
defs:   140 180 320 150
amrs:   . . . 8
dmgs:   100

╒══════╤══════════╤═══════════╤═════════╤═══════════════╤══════════════════════╤══════════╕
│   id │   attack │   defense │   armor │   base_damage │ result               │   damage │
╞══════╪══════════╪═══════════╪═════════╪═══════════════╪══════════════════════╪══════════╡
│    0 │      280 │       140 │       0 │           100 │ DAMAGE: 140          │      140 │
├──────┼──────────┼───────────┼─────────┼───────────────┼──────────────────────┼──────────┤
│    1 │      280 │       180 │       0 │           100 │ DAMAGE: 100          │      100 │
├──────┼──────────┼───────────┼─────────┼───────────────┼──────────────────────┼──────────┤
│    2 │      280 │       320 │       0 │           100 │ COUNTERATTACK: +20 C │        0 │
├──────┼──────────┼───────────┼─────────┼───────────────┼──────────────────────┼──────────┤
│    3 │      280 │       150 │       8 │           100 │ DAMAGE: 50           │       50 │
╘══════╧══════════╧═══════════╧═════════╧═══════════════╧══════════════════════╧══════════╛
╒═════════╕
│   Total │
╞═════════╡
│     290 │
╘═════════╛
```

### crit

Calculates the effects of a critical, or reports that a critical has no effects. If the critical involves amputation, the location is randomly chosen unless specified (by an integer value corresponding to Table 48 of the core book).

`usage: crit level phr_roll location_id`

| field       | type | default | description                                                                                                                                                                                                                                                                                   |
| ----------- | ---- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| level       | int  | 0       | The damage dealt by the attack that triggered the critical roll, plus 1d100 rolled by the attacker. Note that if this value is over 200, the script automatically reduces the value in excess of 200 by half, per the rules for criticals given in the core book.                             |
| phr_roll    | int  | 0       | The final result of the victim's Physical Resistance roll.                                                                                                                                                                                                                                    |
| attack_roll | int  | 0       | The defender's Armor on the Table corresponding to the attacker's attack.                                                                                                                                                                                                                     |
| location_id | int  | 0       | A way of specifying the location of the critical, if for example the attacker was targeting a specific region of the body. See Table 48 on Page 90 of the core book to look up locations, or simply ignore the output of the program with respect to location if one has already been chosen. |

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
