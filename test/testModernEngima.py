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
        self.machine.adjustMachineSettings()


