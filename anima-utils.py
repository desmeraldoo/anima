import cmd
import csv
import math
import random
import sys

DEFAULT_PARTY_FILE = 'my-campaign.csv'
DIFFICULTIES = [20, 40, 80, 120, 140, 180, 240, 280, 320, 440]
SHOCK_CONSEQUENCES = [
    '\n\t-1 Mental Health',
    '\n\t-2 Mental Health',
    '\n\t-3 Mental Health',
    '\n\t-5 Mental Health',
    '\n\t-8 Mental Health',
    '\n\t-10 Mental Health',
    '\n\t-15 Mental Health\n\tPHYSICAL SHOCK 60',
    '\n\t-20 Mental Health\n\tPHYSICAL SHOCK 80\n\tMINOR TEMPORARY DERANGEMENT',
    '\n\t-30 Mental Health\n\tPHYSICAL SHOCK 100\n\tMINOR TEMPORARY DERANGEMENT',
    '\n\t-40 Mental Health\n\tPHYSICAL SHOCK 120\n\tMAJOR TEMOPRARY DERANGEMENT',
    '\n\t-50 Mental Health\n\tPHYSICAL SHOCK 140\n\tMAJOR TEMPORARY DERANGEMENT'
]

def parse(arg):
    '''Convert a series of zero or more numbers to an argument tuple'''
    return tuple(map(int, arg.split()))

def roll(score, open_roll=0):
    base_roll = random.randint(1, 100)
    if base_roll >= (90 + open_roll):
        print('OPEN ROLL!')
        return roll(score + base_roll, open_roll + 1)
    elif (open_roll < 1) and ((score < 200 and base_roll < 4) or (base_roll < 3)):
        print('FUMBLE...')
        return base_roll - random.randint(1, 100)
    else:
        return score + base_roll

def calc_attack(attack, defense, armor=0, base_damage=None):
    result = attack - defense
    if result > 29:
        damage_multiple = None
        
        if armor < 2 and result < 50:
            # special rules for absorption
            if armor == 1:
                if result < 40:
                    damage_multiple = 0.1
                else:
                    damage_multiple = 0.3
            else:
                if result < 40:
                    damage_multiple = 0.1
                else:
                    damage_mtuliple = 0.2
        else:
            damage_multiple = ((result // 10) / 10) - (armor * 0.1)
        
        if damage_multiple <= 0:
            return 'DEFLECTED'
        elif not base_damage:
            return f'ATTACK: {int(damage_multiple * 100)}%'
        else:
            return f'DAMAGE: {int(round(base_damage * damage_multiple, 0))}'
    elif result < 0:
        counterattack_bonus = ((round(abs(result), -1) // 2)) - 5
        return f'COUNTERATTACK: +{counterattack_bonus} C'
    else:
        return 'MISSED'

def calc_crit(damage_dealt, phr_roll, modifier=0, location_level=0):
    crit_level = damage_dealt + random.randint(1, 100) + modifier
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

def calc_shock(composure, willpower, modifier=0):
    if modifier < 8:
        composure_difficulty = DIFFICULTIES[modifier + 1]
    else:
        composure_difficulty = DIFFICULTIES[-2]
    composure_roll = roll(composure)
    if composure_roll > composure_difficulty:
        return 'RESISTED: COMPOSURE'
    
    shock_level = (willpower + random.randint(1, 10)) - (10 + modifier)
    s = f'Level of failure: {shock_level}'
    if shock_level > -1:
        return s + '\n\tRESISTED: WILLPOWER'
    elif shock_level > -11:
        return s + SHOCK_CONSEQUENCES[abs(shock_level) - 1]
    else:
        return s + SHOCK_CONSEQUENCES[-1]

def group_shock(modifier):
    with open(DEFAULT_PARTY_FILE) as csvfile:
        reader = csv.DictReader(csvfile)
        s = []
        for row in reader:
            s.append(row['name'])
            s.append(calc_shock(int(row['composure']), int(row['willpower']), modifier))
    return '\n'.join(s)

class AnimaShell(cmd.Cmd):
    intro = 'Engaging Anima toolkit'
    prompt = '(anima) '
    
    def default(self, _):
        print('Input not recognized.')
    
    def do_attack(self, arg):
        'usage: attack_roll defense_roll [armor] [base_damage]'
        print(calc_attack(*parse(arg)))
    
    def do_crit(self, arg):
        'usage: damage_dealt phr_roll [modifier] [location_level]'
        print(calc_crit(*parse(arg)))
    
    def do_shock(self, arg):
        print(calc_shock(*parse(arg)))
    
    def do_groupshock(self, arg):
        print(group_shock(*parse(arg)))
        
    def do_exit(self, arg):
        'terminate session'
        print('Ending session')
        return True

if __name__ == '__main__':
    AnimaShell().cmdloop()