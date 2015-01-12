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
        self.cipherStock=self.createSampleStock(5)
        l1Stock=self.createSampleStock(3)
        l2Stock=self.createSampleStock(2)
        l1l2Mapper=MapperSwitch(Wiring())
        self.machine=ModernEnigma(self.cipherStock,reflector,plugboard,l1Stock,l2Stock,l1l2Mapper)

    def createSampleStock(self,count):
        cipherStock=[]
        for i in range(count):
            cipherStock.append(Rotor(i,Wiring()))
        return cipherStock
    def testGenerateDefaultSettingsForMachine(self):
        memento=self.manager.generateDefaultSettingsForMachine(self.machine)
        self.assertIsNotNone(memento.cipherRotorStg["ORDER"])
        self.assertIsNotNone(memento.cipherRotorStg["OFFSET"])
        self.assertIsNotNone(memento.activeSwapSignals["SIGNALS"])
        self.assertIsNotNone(memento.activeSwapSignals["CYCLE_STEP"])
        self.assertIsNotNone(memento.swappingL1Stg["ORDER"])
        self.assertIsNotNone(memento.swappingL1Stg["OFFSET"])
        self.assertIsNotNone(memento.swappingL2Stg["ORDER"])
        self.assertIsNotNone(memento.swappingL2Stg["OFFSET"])
        self.assertIsNotNone(memento.L1L2MapperStg["OFFSET"])
        self.assertIsNotNone(memento.L2CipherMapperStg["wiring"])


    def testRandomSettingsForMachine(self):
        memento=self.manager.generateRandomSettingsForMachine(self.machine)
        self.assertIsNotNone(memento.cipherRotorStg["ORDER"])
        self.assertIsNotNone(memento.cipherRotorStg["OFFSET"])
        self.assertIsNotNone(memento.activeSwapSignals["SIGNALS"])
        self.assertIsNotNone(memento.activeSwapSignals["CYCLE_STEP"])
        self.assertIsNotNone(memento.swappingL1Stg["ORDER"])
        self.assertIsNotNone(memento.swappingL1Stg["OFFSET"])
        self.assertIsNotNone(memento.swappingL2Stg["ORDER"])
        self.assertIsNotNone(memento.swappingL2Stg["OFFSET"])
        self.assertIsNotNone(memento.L1L2MapperStg["OFFSET"])
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

    def testGenerateRandomSettingsForMapper(self):
        fromRange=[0,1,2,3,4,5,6]
        toRange=[0,1,2,3]
        result=self.manager.generateRandomSettingsForMapper(fromRange,toRange)
        for f in fromRange:
            self.assertTrue(f in result["wiring"])
    def testGenerateRandomSettingsForRotorStock(self):
        stock=[]
        for i in range(3):
            stock.append(Rotor(i,Wiring()))
        stockStg=self.manager.generateRandomSettingsForRotorStock(stock)
        self.assertIsNotNone(stockStg["ORDER"])
        self.assertIsNotNone(stockStg["OFFSET"])


    def testGenerateDefaultSettingsForRotorStock(self):
        stock=[]
        for i in range(3):
            stock.append(Rotor(i,Wiring()))
        stockStg=self.manager.generateDefaultSettingsForRotorStock(stock)
        self.assertEqual(3,len(stockStg["ORDER"]))

    def testApplyMachineSetting(self):
        defaultStg=self.manager.generateDefaultSettingsForMachine(self.machine)
        self.machine.settingsReady=False
        self.manager.applyMachineSettings(self.machine,defaultStg)
        self.assertTrue(self.machine.settingsReady)
    def testExtractRotorsSettingsFromRotorList(self):
        result=self.manager.extractRotorSettingsFromRotorList(self.cipherStock)
        self.assertEqual(5,len(result["ORDER"]))
        self.assertEqual(5,len(result["OFFSET"]))

    def testBackupMachineSettings(self):
        self.machine.adjustMachineSettings()
        memento=MachineSettingManager.backupMachineSettings(self.machine)

        self.assertIsNotNone(memento.plugboardStg["wiring"])
        self.assertIsNotNone(memento.cipherRotorStg["ORDER"])
        self.assertIsNotNone(memento.cipherRotorStg["OFFSET"])
        self.assertIsNotNone(memento.swappingL1Stg["ORDER"])
        self.assertIsNotNone(memento.swappingL1Stg["OFFSET"])
        self.assertIsNotNone(memento.swappingL2Stg["ORDER"])
        self.assertIsNotNone(memento.swappingL2Stg["OFFSET"])
        self.assertIsNotNone(memento.L1L2MapperStg["OFFSET"])
        self.assertIsNotNone(memento.L2CipherMapperStg["wiring"])



