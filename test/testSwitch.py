import unittest
from Switch import Switch
from Wiring import Wiring

class TestSwitch(unittest.TestCase):
    def setUp(self):
        self.wiringCfg={
            "0": [
                0
            ],
            "1": [
                2
            ],
            "2": [
                1
            ]
        }
        self.switch=Switch(Wiring(self.wiringCfg))
    def testSignal(self):
        self.assertEqual(0,self.switch.signalIn(0))
        self.assertEqual(2,self.switch.signalIn(1))
        self.assertEqual(1,self.switch.signalIn(2))

    def testReverseSignal(self):
        self.assertEqual(0,self.switch.reverseSignal(0))
        self.assertEqual(2,self.switch.reverseSignal(1))
        self.assertEqual(1,self.switch.reverseSignal(2))

