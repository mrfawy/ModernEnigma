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
        self.cipherRotorIds=["0","1","2","3","4"]
        swapStock=self.createSampleStock(3)
        self.machine=ModernEnigma(self.cipherStock,reflector,plugboard,swapStock)

    def createSampleStock(self,count):
        cipherStock={}
        for i in range(count):
            cipherStock[str(i)]=Rotor(i,Wiring())
        return cipherStock
    def testGenerateDefaultSettingsForMachine(self):
        memento=self.manager.generateDefaultSettingsForMachine(self.machine)
        self.assertIsNotNone(memento.cipherRotorStg["ORDER"])
        self.assertIsNotNone(memento.cipherRotorStg["OFFSET"])
        self.assertIsNotNone(memento.activeSwapSignals["SIGNALS"])
        self.assertIsNotNone(memento.activeSwapSignals["CYCLE_STEP"])
        self.assertIsNotNone(memento.swappingRotorStg["ORDER"])
        self.assertIsNotNone(memento.swappingRotorStg["OFFSET"])


    def testRandomSettingsForMachine(self):
        memento=self.manager.generateRandomSettingsForMachine(self.machine)
        self.assertIsNotNone(memento.cipherRotorStg["ORDER"])
        self.assertIsNotNone(memento.cipherRotorStg["OFFSET"])
        self.assertIsNotNone(memento.activeSwapSignals["SIGNALS"])
        self.assertIsNotNone(memento.activeSwapSignals["CYCLE_STEP"])
        self.assertIsNotNone(memento.swappingRotorStg["ORDER"])
        self.assertIsNotNone(memento.swappingRotorStg["OFFSET"])

    def testGenerateRandomSettingsForRotorStock(self):
        stock={}
        for i in range(3):
            stock[str(i)]=Rotor(i,Wiring())
        stockStg=self.manager.generateRandomSettingsForRotorStock(stock)
        self.assertIsNotNone(stockStg["ORDER"])
        self.assertIsNotNone(stockStg["OFFSET"])


    def testGenerateDefaultSettingsForRotorStock(self):
        stock={}
        for i in range(3):
            stock[str(i)]=Rotor(i,Wiring())
        stockStg=self.manager.generateDefaultSettingsForRotorStock(stock)
        self.assertEqual(3,len(stockStg["ORDER"]))

    def testApplyMachineSetting(self):
        defaultStg=self.manager.generateDefaultSettingsForMachine(self.machine)
        self.machine.settingsReady=False
        self.manager.applyMachineSettings(self.machine,defaultStg)
        self.assertTrue(self.machine.settingsReady)

    def testExtractRotorsSettingsFromRotorList(self):
        result=self.manager.extractRotorSettingsFromRotorList(self.cipherStock,self.cipherStock)
        self.assertEqual(5,len(result["ORDER"]))
        self.assertEqual(5,len(result["OFFSET"]))

    def testBackupMachineSettings(self):
        self.machine.adjustMachineSettings()
        memento=MachineSettingManager.backupMachineSettings(self.machine)

        self.assertIsNotNone(memento.plugboardStg["wiring"])
        self.assertIsNotNone(memento.cipherRotorStg["ORDER"])
        self.assertIsNotNone(memento.cipherRotorStg["OFFSET"])
        self.assertIsNotNone(memento.swappingRotorStg["ORDER"])
        self.assertIsNotNone(memento.swappingRotorStg["OFFSET"])



