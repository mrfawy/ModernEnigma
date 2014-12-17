import unittest
from CharIndexMap import CharIndexMap
from EnigmaDynamicFactory import EnigmaDynamicFactory
from Level import Level
from LevelEncryptor import LevelEncryptor
import json

class TestLevelEncryptor(unittest.TestCase):
    def setUp(self):
        self.baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCb")
        self.levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCm")
        self.level=Level(self.baseMachine.getMachineSettings(),self.levelMachine.getMachineSettings())
        self.levelEncryptor=LevelEncryptor(self.baseMachine,self.levelMachine,self.level)
    def testOK(self):
        msg="AAAAA"
        self.level.inputMsg=msg
        resultLevel=self.levelEncryptor.encryptLevel()
        ENC="""BS=IV5K,R-K5~3,9U?K<'\"XCBVW~?N?D'P9<#?8T[^/X[X"""
        self.assertEqual(resultLevel.outputMsg,ENC)
        # print(resultLevel.toJson())

