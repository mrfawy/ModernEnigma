import unittest
from Rotor import Rotor
from PlugBoard import PlugBoard
from Reflector import Reflector
from MapperSwitch import MapperSwitch
from Wiring import Wiring
from MachineSettingManager import MachineSettingManager
from ModernEnigma import ModernEnigma

class TestMachineSettingManager(unittest.TestCase):
    def setUp(self):
        self.manager=MachineSettingManager()
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
    def testGenerateDefaultSettingsForMachine(self):
        memento=self.manager.generateDefaultSettingsForMachine(self.machine)
        self.assertIsNotNone(memento.cipherRotorStg["ORDER"])
        self.assertIsNotNone(memento.cipherRotorStg["OFFSET"])
        self.assertIsNotNone(memento.swappingL1Stg["ORDER"])
        self.assertIsNotNone(memento.swappingL1Stg["OFFSET"])
        self.assertIsNotNone(memento.swappingL2Stg["ORDER"])
        self.assertIsNotNone(memento.swappingL2Stg["OFFSET"])
        self.assertIsNotNone(memento.L1L2MapperStg["wiring"])
        self.assertIsNotNone(memento.L2CipherMapperStg["wiring"])


    def testGenerateDefaultSettingsForMapper_LargeToSmall(self):
        fromRange=range(5)
        toRange=range(2)
        mappingStg=self.manager.gererateDefaultSettingsForMapper(fromRange,toRange)["wiring"]
        self.assertEqual(5,len(mappingStg))
        self.assertEqual(1,len(mappingStg[0]))
        self.assertEqual(1,len(mappingStg[1]))
        self.assertEqual(1,len(mappingStg[2]))

    def testGenerateDefaultSettingsForMapper_SmallToLarge(self):
        fromRange=range(2)
        toRange=range(5)
        mappingStg=self.manager.gererateDefaultSettingsForMapper(fromRange,toRange)["wiring"]
        self.assertEqual(2,len(mappingStg))
        self.assertEqual(3,len(mappingStg[0]))
        self.assertEqual(2,len(mappingStg[1]))

    def testGenerateDefaultSettingsForRotorStock(self):
        stock=[]
        for i in range(3):
            stock.append(Rotor(i,Wiring()))
        stockStg=self.manager.generateDefaultSettingsForRotorStock(stock)
        self.assertEqual(3,len(stockStg["ORDER"]))
