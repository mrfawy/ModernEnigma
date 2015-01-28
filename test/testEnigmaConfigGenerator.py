import unittest
from EnigmaConfigGenerator import EnigmaConfigGenerator
from Util import Util


class TestEnigmaConfigGenerator(unittest.TestCase):
    def setUp(self):
        self.generator=EnigmaConfigGenerator()
        self.seq=["0","1","2","3"]
    def testCreateRandomModelName(self):
        name=self.generator.createRandomModelName(30)
        self.assertEqual(30,len(name))
        name=self.generator.createRandomModelName(3,100)
        self.assertEqual(7,len(name))
        self.assertEqual("|100",name[3::])

    def testCreateEnigmaMachineFromModel(self):
        pass
    def testGetShuffledSequence(self):
        oldSeq=["1","2","3"]
        self.generator.random.seed(123)
        seq=self.generator.getShuffledSequence(oldSeq)
        self.assertEqual(3,len(seq))
        self.assertNotEqual(seq,oldSeq)
    def testCreateWiringCfg_singleOutput(self):
        singleOutput=self.generator.createWiringCfg(range(10),range(10))
        self.assertEqual(10,len(singleOutput))
        for key,val in singleOutput.items():
            self.assertEqual(1,len(val))

    def testCreateWiringCfg_MultiOutput(self):
        wiringCfg=self.generator.createWiringCfg(range(5),range(2))
        self.assertEqual(5,len(wiringCfg))

    def testCreateNotchConfig(self):
        notchCfg=self.generator.createNotchConfig(self.seq,2)
        self.assertEqual(2,len(notchCfg))

    def testGetValidReflectorShuffledWiringCfg(self):
        wiringCfg=self.generator.getValidReflectorShuffledWiringCfg(self.seq)
        self.assertEqual(4,len(wiringCfg))
        for i in self.seq:
            paired=wiringCfg[i][0]
            self.assertEqual(i,wiringCfg[paired][0])

    def testCreateRotorCfg(self):
        rotorCfg=self.generator.createRotorConfig(0,len(self.seq))
        self.assertEqual(len(self.seq),len(rotorCfg["wiring"]))
        self.assertIsNotNone(rotorCfg["notch"])

    def testCreateRotorStockCfg(self):
        rotorStock=self.generator.createRotorStockConfig(7,13)
        self.assertIsNotNone(rotorStock)
        self.assertEqual(7,len(rotorStock))

    def testCreateCipherModuleCfg(self):
        moduleCfg=self.generator.createCipherModuleConfig()
        self.assertIsNotNone(moduleCfg["ROTOR_STOCK"])
        self.assertIsNotNone(moduleCfg["REFLECTOR"])

    def testCreateSwappModuleCfg(self):
        moduleCfg=self.generator.createSwappingModuleConfig()
        self.assertIsNotNone(moduleCfg)
        self.assertIsNotNone(moduleCfg["L1_ROTOR_STOCK"])
        self.assertIsNotNone(moduleCfg["L2_ROTOR_STOCK"])
        self.assertIsNotNone(moduleCfg["L1_L2_MAPPER"])

    def testCreateMachineConfig(self):
        machineCfg=self.generator.createMachineConfig("MCx")
        self.assertIsNotNone(machineCfg)
        self.assertIsNotNone(machineCfg["CIPHER_MODULE"])
        self.assertIsNotNone(machineCfg["SWAPPING_MODULE"])


    def testCreateMapperCfg(self):
        fromRange=[0,1,2,3,4,5,6,7,8,9]
        toRange=[0,1,2]
        mapperCfg=self.generator.createMapperCfg(0,fromRange,toRange)
        self.assertEqual(len(fromRange), len(mapperCfg["wiring"]))

        wiringMap=mapperCfg["wiring"]
        for f in fromRange:
            self.assertTrue(self.existsInKeys(f,wiringMap))
        for t in toRange:
            self.assertTrue(self.existsInValues(t,wiringMap))

    def existsInValues(self,x,wiringMap):
        exists=False
        for pinIn,poutList in wiringMap.items():
            if x in poutList:
                return True
        return exists
    def existsInKeys(self,x,wiringMap):
        exists=False
        for pinIn,poutList in wiringMap.items():
            if x == pinIn:
                return True
        return exists

