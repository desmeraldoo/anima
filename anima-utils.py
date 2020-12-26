import cmd
import csv
import math
import random
import sys

DEFAULT_PARTY_FILE = 'my-campaign.csv'
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

def parse(args):
    '''Convert a series of zero or more numbers to an argument tuple'''
    return tuple(map(int, args.split()))

def roll(score, modifier=0, open_roll=0):
    base_roll = random.randint(1, 100)
    if base_roll >= (90 + open_roll) or base_roll == 100:
        return score + base_roll + modifier + roll(0, open_roll=open_roll + 1)
    elif (open_roll < 1) and ((score < 200 and base_roll < 4) or (base_roll < 3)):
        return score + base_roll + modifier - random.randint(1, 100)
    else:
        return score + base_roll + modifier

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

def calc_shock(composure, willpower, difficulty=10):
    # This is a homebrew difficulty calculation that does not reflect the
    # system as described in the Master's Tookit, which I found inconsistent. I
    # tried to make it as similar as possible.
    composure_difficulty = 20 + (difficulty * 10)
    composure_roll = roll(composure)
    s = f'Composure roll {composure_roll} against difficulty {composure_difficulty}'
    if composure_roll > composure_difficulty:
        return s + '\n\tRESISTED: COMPOSURE'
    
    shock_level = (willpower + random.randint(1, 10)) - (difficulty)
    s += f'\nLevel of failure: {shock_level}'
    if shock_level > -1:
        return s + '\n\tRESISTED: WILLPOWER'
    elif shock_level > -11:
        return s + SHOCK_CONSEQUENCES[abs(shock_level) - 1]
    else:
        return s + SHOCK_CONSEQUENCES[-1]

def group_shock(difficulty=10):
    with open(DEFAULT_PARTY_FILE) as csvfile:
        reader = csv.DictReader(csvfile)
        s = []
        for row in reader:
            s.append(row['name'])
            s.append(calc_shock(int(row['composure']), int(row['willpower']), difficulty))
    return '\n'.join(s)

def calc_notice(notice, difficulty, modifier=0):
    notice_score = roll(notice, modifier)
    return notice_score > difficulty
    
def group_notice(difficulty, modifier=0):
    with open(DEFAULT_PARTY_FILE) as csvfile:
        reader = csv.DictReader(csvfile)
        s = []
        for row in reader:
            s.append(row['name'])
            s.append(': ')
            s.append(calc_notice(int(row['notice']), difficulty, modifier))
            s.append('\n')
    return ' '.join(s)

class AnimaShell(cmd.Cmd):
    intro = 'Engaging Anima toolkit'
    prompt = '(anima) '
    
    def default(self, _):
        print('Input not recognized.')
    
    def do_attack(self, args):
        'usage: attack_roll defense_roll [armor] [base_damage]'
        print(calc_attack(*parse(args)))
    
    def do_crit(self, args):
        'usage: damage_dealt phr_roll [modifier] [location_level]'
        print(calc_crit(*parse(args)))
    
    def do_shock(self, args):
        'usage: composure willpower [difficulty=10]'
        print(calc_shock(*parse(args)))
    
    def do_groupshock(self, args):
        'usage: [difficulty=10]\nrequires user-defined file \'my-campaign.csv\' (see docs)'
        print(group_shock(*parse(args)))
    
    def do_notice(self, args):
        'usage: notice difficulty [modifier=0]'
        print(calc_notice(*parse(args))
    
    def do_groupnotice(self, args):
        'usage: difficulty [modifier=0]'
        
    def do_exit(self, args):
        'terminate session'
        print('Ending session')
        return True

if __name__ == '__main__':
    AnimaShell().cmdloop()