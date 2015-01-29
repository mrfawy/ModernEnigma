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
        swapStock=self.createSampleStock(3)
        self.machine=ModernEnigma(cipherStock,reflector,plugboard,swapStock)

    def createSampleStock(self,count):
        cipherStock={}
        for i in range(count):
            cipherStock[i]=Rotor(i,Wiring())
        return cipherStock

    def testAdjustMachineSettings(self):
        self.assertFalse(self.machine.settingsReady)
        self.machine.adjustMachineSettings()
        self.assertTrue(self.machine.settingsReady)

    def testApplyActivePins(self):
        rotors={}
        rotors[0]=Rotor(0,Wiring({0:[1],2:[5],1:[1],3:[3],4:[4],5:[5]}))
        rotors[1]=Rotor(1,Wiring({1:[3],3:[2],0:[0],2:[2],4:[4],5:[5]}))
        rotors[2]=Rotor(2,Wiring({3:[5],5:[3],0:[0],1:[1],2:[2],4:[4]}))
        rotorIds=[0,1,2]
        resultPins=self.machine.applyActivePins(rotorIds,rotors,[0])
        self.assertEqual([5],resultPins)

    def testApplyActivePinsReversed(self):
        rotors={}
        rotors[0]=Rotor(0,Wiring({0:[1],2:[5],1:[1],3:[3],4:[4],5:[0]}))
        rotors[1]=Rotor(1,Wiring({1:[3],3:[2],0:[0],2:[2],4:[4],5:[5]}))
        rotors[2]=Rotor(2,Wiring({3:[5],5:[3],0:[0],1:[1],2:[2],4:[4]}))
        rotorIds=[0,1,2]
        resultPins=self.machine.applyActivePinsReversed(rotorIds,rotors,[0])
        self.assertEqual([5],resultPins)

    def testProcessStepping(self):
        rotors={}
        rotors[0]=Rotor(0,Wiring(),[0,1])
        rotors[1]=Rotor(1,Wiring(),[1])
        rotors[2]=Rotor(2,Wiring(),[0,2])

        rotorIds=[0,1,2]
        self.assertEqual([0,0,0],[rotors[0].offset,rotors[1].offset,rotors[2].offset])
        self.machine.processStepping(rotorIds,rotors)
        self.assertEqual([1,1,1],[rotors[0].offset,rotors[1].offset,rotors[2].offset])
        self.machine.processStepping(rotorIds,rotors)
        self.assertEqual([2,1,1],[rotors[0].offset,rotors[1].offset,rotors[2].offset])

    def testProcessRotorSwapping(self):
        raise ("Test case need to be writted ")


    def testAdjustWindowDisplay(self):
        rotors={}
        rotors[0]=Rotor(0,Wiring())
        rotors[1]=Rotor(1,Wiring())
        rotors[2]=Rotor(2,Wiring())
        rotorIds=[0,1,2]
        self.assertEqual([0,0,0],[rotors[0].offset,rotors[1].offset,rotors[2].offset])
        self.machine.cipherRotorIdList=rotorIds
        self.machine.cipherRotorStockMap=rotors
        self.machine.adjustWindowDisplay([3,2,1])
        self.assertEqual([3,2,1],[rotors[0].offset,rotors[1].offset,rotors[2].offset])


