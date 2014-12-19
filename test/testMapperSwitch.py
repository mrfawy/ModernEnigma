import unittest
from MapperSwitch import MapperSwitch
from Wiring import Wiring

class TestMapperSwitch(unittest.TestCase):
    def setUp(self):
        self.wiringCfg={
            "0": [
                0
            ],
            "1": [
                2,0
            ],
            "2": [
                1,0
            ]
        }
        self.mapper=MapperSwitch(Wiring(self.wiringCfg))
    def testSignal(self):
        self.assertEqual(1,len(self.mapper.signalIn(0)))
        self.assertEqual(2,len(self.mapper.signalIn(1)))

    def testinvalidOperation(self):
        with self.assertRaises(Exception) as c:
            self.mapper.reverseSignal(0)

