import unittest
from CharIndexMap import CharIndexMap
from EnigmaDynamicFactory import EnigmaDynamicFactory
from Level import Level
from LevelDecryptor import LevelDecryptor
from LevelEncryptor import LevelEncryptor
import json

class TestLevelDecryptor(unittest.TestCase):
    def setUp(self):
        self.baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCb")
        self.levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCm")
        self.level=Level(self.baseMachine.getMachineSettings(),self.levelMachine.getMachineSettings())
        self.levelDecryptor=LevelDecryptor(self.baseMachine,self.levelMachine,self.level)
    def testDualOK(self):
        msg="AAAAA"
        self.level.inputMsg=msg
        levelEncryptor=LevelEncryptor(self.baseMachine,self.levelMachine,self.level)
        encLevel=levelEncryptor.encryptLevel()
        encLevel.inputMsg=""
        self.levelDecryptor.level=encLevel
        resultLevel=self.levelDecryptor.decryptLevel()
        self.assertEqual(resultLevel.inputMsg,msg)
        # print(resultLevel.toJson())

