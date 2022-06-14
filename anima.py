import cmd
import csv
import math
import random
import sys
import pdb
import traceback

from const import *

def parse(args):
    '''Convert a series of zero or more numbers to an argument tuple'''
    return tuple(map(int, args.split()))

def calc_damage_multiple(result, armor):
    '''NOTE: Assumes result is greater than 0.'''
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
    if level > 200: level -= (level - 200) // 2
    level -= phr_roll
    
    if not location_id: location_id = random.randint(1, 100)
    location = ''
    if location_id < 11:
        location = 'Torso (Ribs)'
    elif location_id < 21:
        location = 'Torso (Shoulder)'
    elif location_id < 31:
        location = 'Torso (Stomach)'
    elif location_id < 36:
        location = 'Torso (Kidneys)'
    elif location_id < 49:
        location = 'Torso (Chest)'
    elif location_id < 51:
        location = 'Torso (Heart)'
    elif location_id < 55:
        location = 'Right arm (Upper forearm)'
    elif location_id < 59:
        location = 'Right arm (Lower forearm)'
    elif location_id < 61:
        location = 'Right arm (Hand)'
    elif location_id < 65:
        location = 'Left arm (Upper forearm)'
    elif location_id < 69:
        location = 'Left arm (Lower forearm)'
    elif location_id < 71:
        location = 'Left arm (Hand)'
    elif location_id < 75:
        location = 'Right leg (Thigh)'
    elif location_id < 79:
        location = 'Right leg (Calf)'
    elif location_id < 81:
        location = 'Right leg (Foot)'
    elif location_id < 85:
        location = 'Left leg (Thigh)'
    elif location_id < 89:
        location = 'Left leg (Calf)'
    elif location_id < 91:
        location = 'Left leg (Foot)'
    else:
        location = 'Head'
    
    s = f'CRIT LEVEL {level}'    
    if level < 1:
        return s + '\n\tNO FURTHER EFFECT'
    elif level < 51:
        return s + f'\n\tMINOR CRITICAL\n\tALL ACTION PENALTY (-{level})'
    else:
        s += f'\n\tMAJOR CRITICAL [{location}]\n\tALL ACTION PENALTY (-{level // 2})\n\tALL ACTION SACRIFICE (-{level // 2})'
        
        if level > 100:
            if location_id > 90 or (location_id == 49 or location_id == 50):
                s += '\n\tINSTANT DEATH'
            elif location_id > 50 and location_id < 91:
                s += '\n\tAMPUTATION'
        
            if level > 150:
                s += '\n\tUNCONCIOUS -- AT RISK OF DEATH'
        
        return s

def chaotic_powers(num_powers=5):
    return 'CHAOTIC POWERS:\n' + '\n'.join(random.sample(POWERS, num_powers))

def mass_combat(num, lp, damage_resistant=0):
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
    
    def do_mass(self, args):
        'usage: mass [num] [lp] [damage_resistant = 0 | 1]'
        print(mass_combat(*parse(args)))
        
    def do_exit(self, args):
        'terminate session'
        print('Ending session')
        raise KeyboardInterrupt

if __name__ == '__main__':
    while True:
        try:
            AnimaShell().cmdloop()
        except KeyboardInterrupt:
            raise SystemExit(0)
        except:
            traceback.print_exc()