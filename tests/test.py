import unittest

import src.anima.core as core


class TestAnimaUtils(unittest.TestCase):
    def test_attack(self) -> None:
        self.assertEqual(core.calc_attack(255, 0), "ATTACK: 250%")
        self.assertEqual(core.calc_attack(0, 255), "COUNTERATTACK: +125 C")
        self.assertEqual(core.calc_attack(255, 0, 10), "ATTACK: 150%")
        self.assertEqual(core.calc_attack(0, 255, 10), "COUNTERATTACK: +125 C")
        self.assertEqual(core.calc_attack(255, 0, 0, 100), "DAMAGE: 250")
        self.assertEqual(core.calc_attack(0, 255, 0, 10), "COUNTERATTACK: +125 C")
        self.assertEqual(core.calc_attack(255, 0, 10, 100), "DAMAGE: 150")
        self.assertEqual(core.calc_attack(0, 255, 0, 10), "COUNTERATTACK: +125 C")
        self.assertEqual(core.calc_attack(255, 175, 10), "DEFLECTED")
        self.assertEqual(core.calc_attack(255, 175, 10, 100), "DEFLECTED")
        self.assertEqual(core.calc_attack(255, 254), "MISSED")
        self.assertEqual(core.calc_attack(255, 254, 10), "MISSED")
        self.assertEqual(core.calc_attack(255, 254, 10, 100), "MISSED")
        self.assertEqual(core.calc_attack(254, 255), "COUNTERATTACK: +0 C")
        self.assertEqual(core.calc_attack(254, 255, 10), "COUNTERATTACK: +0 C")
        self.assertEqual(core.calc_attack(254, 255, 10, 100), "COUNTERATTACK: +0 C")


if __name__ == "__main__":
    unittest.main()
