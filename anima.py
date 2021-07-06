import cmd
import csv
import math
import random
import sys
import pdb

from const import *

def parse(args):
    '''Convert a series of zero or more numbers to an argument tuple'''
    return tuple(map(int, args.split()))

def calc_damage_multiple(result, armor):
    '''NOTE: Assumes result is greater than 0.'''
    if result > 29:
        if armor < 2 and result < 50:
            # special rules for absorption
            if armor == 1:
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
            return ((result // 10) / 10) - (armor * 0.1)
    else:
        return 0

def calc_attack(attack, defense, armor=0, base_damage=None):
    result = attack - defense
    if result < 0:
        counterattack_bonus = -result // 10 * 5
        return f'COUNTERATTACK: +{counterattack_bonus} C'
    
    damage_multiple = calc_damage_multiple(result, armor)
    if damage_multiple < 0:
        return 'DEFLECTED'
    elif damage_multiple == 0:
        return 'MISSED'
    elif not base_damage:
        return f'ATTACK: {int(damage_multiple * 100)}%'
    else:
        return f'DAMAGE: {int(round(base_damage * damage_multiple, 0))}'

def calc_combo():
    attacks = list(map(int, input('Enter final attack rolls: ').split(' ')))
    defenses = list(map(int, input('Enter final defense rolls: ').split(' ')))
    if len(attacks) != len(defenses):
        return 'ERROR: Number of attacks and defenses do not match. Enter 0 for missing defenses.'
    armor = int(input('Enter armor value (AT): '))
    base_damage = int(input('Enter Base Damage: '))
    
    results = []
    total_damage = 0
    for attack, defense in zip(attacks, defenses):
        if attack > defense:
            damage_multiple = calc_damage_multiple(attack - defense, armor)
            if damage_multiple > 0:
                total_damage += int(round(base_damage * damage_multiple, 0))
        results.append(calc_attack(attack, defense, armor, base_damage))
    return '\n'.join(results) + f'\nTOTAL DAMAGE: {total_damage}'

def calc_crit(level, phr_roll, location_id=0):
    if crit_level > 200: crit_level -= (crit_level - 200) // 2
    crit_level -= phr_roll
    
    if not location_level: location_level = random.randint(1, 100)
    location = ''
    if location_level < 11:
        location = 'Torso (Ribs)'
    elif location_level < 21:
        location = 'Torso (Shoulder)'
    elif location_level < 31:
        location = 'Torso (Stomach)'
    elif location_level < 36:
        location = 'Torso (Kidneys)'
    elif location_level < 49:
        location = 'Torso (Chest)'
    elif location_level < 51:
        location = 'Torso (Heart)'
    elif location_level < 55:
        location = 'Right arm (Upper forearm)'
    elif location_level < 59:
        location = 'Right arm (Lower forearm)'
    elif location_level < 61:
        location = 'Right arm (Hand)'
    elif location_level < 65:
        location = 'Left arm (Upper forearm)'
    elif location_level < 69:
        location = 'Left arm (Lower forearm)'
    elif location_level < 71:
        location = 'Left arm (Hand)'
    elif location_level < 75:
        location = 'Right leg (Thigh)'
    elif location_level < 79:
        location = 'Right leg (Calf)'
    elif location_level < 81:
        location = 'Right leg (Foot)'
    elif location_level < 85:
        location = 'Left leg (Thigh)'
    elif location_level < 89:
        location = 'Left leg (Calf)'
    elif location_level < 91:
        location = 'Left leg (Foot)'
    else:
        location = 'Head'
    
    s = f'CRIT LEVEL {crit_level}'    
    if crit_level < 1:
        return s + '\n\tNO FURTHER EFFECT'
    elif crit_level < 51:
        return s + f'\n\tMINOR CRITICAL\n\tALL ACTION PENALTY (-{crit_level})'
    else:
        s += f'\n\tMAJOR CRITICAL [{location}]\n\tALL ACTION PENALTY (-{crit_level // 2})\n\tALL ACTION SACRIFICE (-{crit_level // 2})'
        
        if crit_level > 100:
            if location_level > 90 or (location_level == 49 or location_level == 50):
                s += '\n\tINSTANT DEATH'
            elif location_level > 50 and location_level < 91:
                s += '\n\tAMPUTATION'
        
            if crit_level > 150:
                s += '\n\tUNCONCIOUS -- AT RISK OF DEATH'
        
        return s

def chaotic_powers(num_powers=5):
    return 'CHAOTIC POWERS:\n' + '\n'.join(random.choices(POWERS, k=num_powers))

class AnimaShell(cmd.Cmd):
    intro = 'Engaging Anima toolkit'
    prompt = '(anima) '
    
    def default(self, _):
        print('Input not recognized.')
    
    def do_attack(self, args):
        'usage: attack attack_roll defense_roll [armor] [base_damage]'
        print(calc_attack(*parse(args)))
        
    def do_combo(self, args):
        'usage: combo\nNOTE: This is an interactive command with multiple inputs. It does not accept arguments.\nNOTE: Remember that combos can be interrupted if a counterattack presents itself, or by other means.'
        print(calc_combo())
    
    def do_crit(self, args):
        'usage: crit level phr_roll [location_id]'
        print(calc_crit(*parse(args)))
    
    def do_chaos(self, args):
        'usage: chaos [num_powers]'
        print(chaotic_powers(*parse(args)))
        
    def do_exit(self, args):
        'terminate session'
        print('Ending session')
        return True

if __name__ == '__main__':
    AnimaShell().cmdloop()