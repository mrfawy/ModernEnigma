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

    def testApplyActivePins(self):
        rotors=[]
        rotors.append(Rotor(0,Wiring({0:[1],2:[5],1:[1],3:[3],4:[4],5:[5]})))
        rotors.append(Rotor(1,Wiring({1:[3],3:[2],0:[0],2:[2],4:[4],5:[5]})))
        rotors.append(Rotor(2,Wiring({3:[5],5:[3],0:[0],1:[1],2:[2],4:[4]})))
        resultPins=self.machine.applyActivePins(rotors,[0])
        self.assertEqual(5,resultPins[0])

    def testApplyActivePinsReversed(self):
        rotors=[]
        rotors.append(Rotor(0,Wiring({0:[1],2:[5],1:[1],3:[3],4:[4],5:[0]})))
        rotors.append(Rotor(1,Wiring({1:[3],3:[2],0:[0],2:[2],4:[4],5:[5]})))
        rotors.append(Rotor(2,Wiring({3:[5],5:[3],0:[0],1:[1],2:[2],4:[4]})))
        resultPins=self.machine.applyActivePinsReversed(rotors,[0])
        self.assertEqual(5,resultPins[0])

    def testProcessStepping(self):
        rotors=[]
        rotors.append(Rotor(0,Wiring(),[0,1]))
        rotors.append(Rotor(1,Wiring(),[1]))
        rotors.append(Rotor(2,Wiring(),[0,2]))
        self.assertEqual([0,0,0],[rotors[0].offset,rotors[1].offset,rotors[2].offset])
        self.machine.processStepping(rotors)
        self.assertEqual([1,1,1],[rotors[0].offset,rotors[1].offset,rotors[2].offset])
        self.machine.processStepping(rotors)
        self.assertEqual([2,1,1],[rotors[0].offset,rotors[1].offset,rotors[2].offset])

    def testProcessRotorSwapping(self):
        l1Rotors=[Rotor(0,Wiring({0:[1],1:[2],2:[3],3:[1]}))]
        l2Rotors=[Rotor(1,Wiring({0:[1],1:[2],2:[3],3:[1]}))]

        self.machine.swapRotorsLevel1=l1Rotors
        self.machine.swapRotorsLevel2=l2Rotors

        self.machine.l1l2Mapper=MapperSwitch(Wiring({0:[0],1:[1],2:[2],3:[3]}))

        self.machine.l2CipherMapper=MapperSwitch(Wiring({0:[0],1:[1],2:[2],3:[3]}))

        rotors=[]
        rotors.append(Rotor(0,Wiring()))
        rotors.append(Rotor(1,Wiring()))
        rotors.append(Rotor(2,Wiring()))
        rotors.append(Rotor(3,Wiring()))

        self.machine.rotorList=rotors

        self.assertEqual(0,self.machine.rotorList[0].id)
        self.assertEqual(1,self.machine.rotorList[1].id)
        self.assertEqual(2,self.machine.rotorList[2].id)
        self.assertEqual(3,self.machine.rotorList[3].id)

        self.machine.swapActiveSignals=[1]

        self.machine.processRotorSwapping(0)
        self.assertEqual(3,self.machine.rotorList[0].id)
        self.assertEqual(1,self.machine.rotorList[1].id)
        self.assertEqual(2,self.machine.rotorList[2].id)
        self.assertEqual(0,self.machine.rotorList[3].id)

    def testProcessActiveSwapSignalsCycleStep(self):
        self.machine.swapActiveSignals=[1,3]
        self.machine.swapActiveSignalsCycleStep=3
        self.machine.swapRotorsLevel1=[]
        self.machine.swapRotorsLevel1.append(Rotor(0,Wiring({0:[0],1:[1],2:[2],3:[3]})))
        self.machine.processActiveSwapSignalsCycleStep()
        self.assertEqual([0,2],self.machine.swapActiveSignals)


    def testAdjustWindowDisplay(self):
        rotors=[]
        rotors.append(Rotor(0,Wiring()))
        rotors.append(Rotor(1,Wiring()))
        rotors.append(Rotor(2,Wiring()))
        self.assertEqual([0,0,0],[rotors[0].offset,rotors[1].offset,rotors[2].offset])
        self.machine.rotorList=rotors
        self.machine.adjustWindowDisplay([3,2,1])
        self.assertEqual([3,2,1],[rotors[0].offset,rotors[1].offset,rotors[2].offset])


    def testSwap(self):
        l=[0,1,2]
        self.machine.swap(l,0,1)
        self.assertEqual([1,0,2],l)
    def testSwapRotors(self):
        l=[0,1,2,3,4,5,6]
        self.machine.swapRotors(l,[1])
        self.assertEqual([0,3,2,1,4,5,6],l)
        self.machine.swapRotors(l,[0])
        self.assertEqual([6,3,2,1,4,5,0],l)
        self.machine.swapRotors(l,[3,0])
        self.assertEqual([0,3,1,2,4,5,6],l)

