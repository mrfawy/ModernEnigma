import unittest
from PlugBoard import PlugBoard
from Rotor import Rotor
from Reflector import Reflector
from CharIndexMap import CharIndexMap
from MapperSwitch import MapperSwitch
from Wiring import Wiring
from RandomGenerator import RandomGenerator
from ModernEnigma import ModernEnigma
from MachineSettingsMemento import MachineSettingsMemento


class TestModernEnigma(unittest.TestCase):
    def setUp(self):
        plugboard=PlugBoard(Wiring())
        reflector=Reflector(Wiring())
        cipherStock=self.createSampleStock(5)
        l1Stock=self.createSampleStock(3)
        l2Stock=self.createSampleStock(2)
        l1l2Mapper=MapperSwitch(Wiring())
        self.machine=ModernEnigma(cipherStock,reflector,plugboard,l1Stock,l2Stock,l1l2Mapper)

    def createSampleStock(self,count):
        cipherStock=[]
        for i in range(count):
            cipherStock.append(Rotor(i,Wiring()))
        return cipherStock

    def testAdjustMachineSettings(self):
        self.assertFalse(self.machine.settingsReady)
        self.machine.adjustMachineSettings()
        self.assertTrue(self.machine.settingsReady)


    def testSwap(self):
        l=[0,1,2]
        self.machine.swap(l,0,1)
        self.assertEqual([1,0,2],l)
    def testSwapRotors(self):
        l=[0,1,2,3]
        self.machine.swapRotors(l,[1])
        self.assertEqual([0,3,2,1],l)
        self.machine.swapRotors(l,[0])
        self.assertEqual([1,3,2,0],l)

