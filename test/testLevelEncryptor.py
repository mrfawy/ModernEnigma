import unittest
from CharIndexMap import CharIndexMap
from EnigmaDynamicFactory import EnigmaDynamicFactory
from Level import Level
from LevelEncryptor import LevelEncryptor
from StreamConverter import CharacterStreamConverter
import json

class TestLevelEncryptor(unittest.TestCase):
    def setUp(self):
        self.baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCb")
        self.levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCm")
        self.level=Level(self.baseMachine.getMachineSettings(),self.levelMachine.getMachineSettings())
        self.levelEncryptor=LevelEncryptor(self.baseMachine,self.levelMachine,self.level)
        self.levelEncryptor.streamConverter=CharacterStreamConverter()
    # def testOK(self):
    #     msg="AAAAA"
    #     self.level.inputMsg=msg
    #     resultLevel=self.levelEncryptor.encryptLevel()
    #     ENC="""BS=IV5K,R-K5~3,9U?K<'\"XCBVW~?N?D'P9<#?8T[^/X[X"""
    #     self.assertEqual(len(resultLevel.outputMsg),len(ENC))
    #     # print(resultLevel.toJson())

    def testGeneratePerMsgWindowSetting(self):
        out=self.levelEncryptor.generatePerMsgWindowSetting(self.baseMachine)
        self.assertEqual(len(self.baseMachine.rotorList),len(out))
    def testPerformMappingBlockToRotor(self):
        seq=[1,1,1,1,1,1,1,1]
        result=[1,257,513,769,1,257,513,769]
        self.assertEqual(result,self.levelEncryptor.performMappingBlockToRotor(seq,4*256))

