import unittest
from MachineSettingsMemento import MachineSettingsMemento

class TestMachineSettingsMemento(unittest.TestCase):

    def setUp(self):
        self.settingStr="01 03 05 | 00 15 18 |0 1 , 2 3 |13 15 |02 03 |22 25 |55 |07 03 | 11 13 |0: 01 03 ,04: 03 02 04"

    def testParseRotorStg(self):
        rotorStg=MachineSettingsMemento.parseRotorStg("01 03 05","00 15 18")
        self.assertIsNotNone(rotorStg["ORDER"])
        self.assertEqual(3 ,len(rotorStg["ORDER"]))
        self.assertEqual(5,rotorStg["ORDER"][-1])

        self.assertIsNotNone(rotorStg["OFFSET"])
        self.assertEqual(3 ,len(rotorStg["OFFSET"]))
        self.assertEqual(18,rotorStg["OFFSET"][-1])

    def testParseMapperStg(self):
        mapperStg=MachineSettingsMemento.parseMapperStg("0: 01 03 ,04: 03 02 04")
        self.assertIsNotNone(mapperStg["wiring"])
        self.assertEqual(3 ,len(mapperStg["wiring"][4]))

    def testInitInstanceFromStg(self):
        result=MachineSettingsMemento.InitInstanceFromStrStg(self.settingStr)

        self.assertIsNotNone(result)
        self.assertIsNotNone(result.cipherRotorStg["ORDER"])
        self.assertIsNotNone(result.cipherRotorStg["OFFSET"])
        self.assertIsNotNone(result.plugboardStg["wiring"])
        self.assertIsNotNone(result.activeSwapSignals)
        self.assertEqual(2,len(result.activeSwapSignals))
        self.assertIsNotNone(result.swappingL1Stg["ORDER"])
        self.assertIsNotNone(result.swappingL1Stg["OFFSET"])
        self.assertIsNotNone(result.swappingL2Stg["ORDER"])
        self.assertIsNotNone(result.swappingL2Stg["OFFSET"])

        self.assertIsNotNone(result.L1L2MapperStg["OFFSET"])
        self.assertIsNotNone(result.L2CipherMapperStg["wiring"])

        def testValidateSettingString(self):
            stg=self.settingStr
            self.assertTrue(MachineSettingsMemento.validateSettingString(stg))

            stg="01 03 05 | 00 15 18 |0 1 , 2 3 |02 03 |22 25 |55 |07 03 "
            self.assertFalse(MachineSettingsMemento.validateSettingString(stg))



