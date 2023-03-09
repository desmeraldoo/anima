import src.anima.commands.attack as attack


def test_attack() -> None:
    assert attack.calc_attack(255, 0) == "ATTACK: 250%"
    assert attack.calc_attack(0, 255) == "COUNTERATTACK: +125 C"
    assert attack.calc_attack(255, 0, 10) == "ATTACK: 150%"
    assert attack.calc_attack(0, 255, 10) == "COUNTERATTACK: +125 C"
    assert attack.calc_attack(255, 0, 0, 100) == "DAMAGE: 250"
    assert attack.calc_attack(0, 255, 0, 10) == "COUNTERATTACK: +125 C"
    assert attack.calc_attack(255, 0, 10, 100) == "DAMAGE: 150"
    assert attack.calc_attack(0, 255, 0, 10) == "COUNTERATTACK: +125 C"
    assert attack.calc_attack(255, 175, 10) == "DEFLECTED"
    assert attack.calc_attack(255, 175, 10, 100) == "DEFLECTED"
    assert attack.calc_attack(255, 254) == "MISSED"
    assert attack.calc_attack(255, 254, 10) == "MISSED"
    assert attack.calc_attack(255, 254, 10, 100) == "MISSED"
    assert attack.calc_attack(254, 255) == "COUNTERATTACK: +0 C"
    assert attack.calc_attack(254, 255, 10) == "COUNTERATTACK: +0 C"
    assert attack.calc_attack(254, 255, 10, 100) == "COUNTERATTACK: +0 C"
