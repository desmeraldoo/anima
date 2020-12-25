import cmd
import math
import random
import sys

def parse(arg):
    '''Convert a series of zero or more numbers to an argument tuple'''
    return tuple(map(int, arg.split()))

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
        
    def do_exit(self, arg):
        'terminate session'
        print('Ending session')
        return True

if __name__ == '__main__':
    AnimaShell().cmdloop()