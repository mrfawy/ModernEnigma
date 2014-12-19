import unittest
from PlugBoard import PlugBoard
from Wiring import Wiring

class TestPlugBoard(unittest.TestCase):
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
    def testInitFromWiring(self):
        pb=PlugBoard(Wiring(self.wiringCfg))
        self.assertIsNotNone(pb)
        self.assertEqual(0,pb.signalIn(0))
        self.assertEqual(2,pb.signalIn(1))
        self.assertEqual(1,pb.signalIn(2))

    def testInitFromInputPairs(self):
        wiringStr="0 0 , 1 2 "
        pb=PlugBoard.initFromString(wiringStr)
        self.assertIsNotNone(pb)
        self.assertEqual(0,pb.signalIn(0))
        self.assertEqual(2,pb.signalIn(1))
        self.assertEqual(1,pb.signalIn(2))

    def testInvalidInputWiringStr(self):
        wiringStr="0 1 , 1 2"
        with self.assertRaises(Exception) as c:
            PlugBoard.initFromString(wiringStr)

    def testSignalIn(self):
        wiringStr="0 0 , 1 2 "
        pb=PlugBoard.initFromString(wiringStr)
        self.assertEqual(0,pb.signalIn(0))
        self.assertEqual(2,pb.signalIn(1))
        self.assertEqual(1,pb.signalIn(2))
        self.assertEqual(9,pb.signalIn(9))
    def testReverseSignal(self):
        wiringStr="0 0 , 1 2 "
        pb=PlugBoard.initFromString(wiringStr)
        self.assertEqual(0,pb.reverseSignal(0))
        self.assertEqual(2,pb.reverseSignal(1))
        self.assertEqual(1,pb.reverseSignal(2))
        self.assertEqual(9,pb.reverseSignal(9))

    def testGetSettingsAsStr(self):
        wiringStr="0 0,1 2"
        pb=PlugBoard.initFromString(wiringStr)
        self.assertEqual(wiringStr,pb.getSettings())




