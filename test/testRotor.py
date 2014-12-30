import unittest
from Rotor import Rotor
from Wiring import Wiring

class TestRotor(unittest.TestCase):
    def setUp(self):
        config={
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
        self.rotor=Rotor(0,Wiring(config),[])

    def testSignalIn(self):
        self.assertEqual([0],self.rotor.signalIn([0]))
        self.rotor.rotate()
        self.assertEqual([1],self.rotor.signalIn([0]))


    def testReverseSignal(self):
        self.assertEqual([0],self.rotor.reverseSignal([0]))
        self.rotor.rotate()
        self.assertEqual([0],self.rotor.reverseSignal([1]))
    def testRotate(self):
        self.assertEqual(0,self.rotor.offset)
        self.rotor.rotate()
        self.assertEqual(1,self.rotor.offset)

    def testAdjustDisplay(self):
        self.rotor.adjustDisplay(2)
        self.assertEqual(2,self.rotor.offset)
        self.assertEqual([2],self.rotor.signalIn([0]))


