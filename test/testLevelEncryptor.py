import unittest
from CharIndexMap import CharIndexMap
from EnigmaDynamicFactory import EnigmaDynamicFactory
from Level import Level
from LevelEncryptor import LevelEncryptor
from Util import Util
import json

class TestLevelEncryptor(unittest.TestCase):
    def setUp(self):
        self.baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCb")
        self.baseMachine.adjustMachineSettings()
        self.levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCm")
        self.levelMachine.adjustMachineSettings()
        self.level=Level(self.baseMachine.getMachineSettings(),self.levelMachine.getMachineSettings())
        self.levelEncryptor=LevelEncryptor(self.baseMachine,self.levelMachine,self.level)
    def testOK(self):
        msg="AAAAA"
        msgSeq=Util.encodeStringIntoByteList(msg)
        self.level.inputMsg=msgSeq
        resultLevel=self.levelEncryptor.encryptLevel()
        decMsg=Util.decodeByteListIntoString(resultLevel.inputMsg)
        self.assertEqual(msg,decMsg)

    def testGeneratePerMsgWindowSetting(self):
        out=self.levelEncryptor.generatePerMsgWindowSetting(self.baseMachine)
        self.assertEqual(len(self.baseMachine.rotorList),len(out))

    def testApplyXor(self):
        seq=[1,2,3,4]
        result=self.levelEncryptor.applyXor(seq,40)
        self.assertNotEqual(result,seq)
        "if xored again should return original value"
        self.assertEqual(seq,self.levelEncryptor.applyXor(result,40))

