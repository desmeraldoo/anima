import random


def crit(level: int, phr_roll: int, location_id: int = 0) -> str:
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
