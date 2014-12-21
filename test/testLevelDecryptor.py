import unittest
from CharIndexMap import CharIndexMap
from EnigmaDynamicFactory import EnigmaDynamicFactory
from Level import Level
from LevelDecryptor import LevelDecryptor
from LevelEncryptor import LevelEncryptor
from StreamConverter import CharacterStreamConverter
from RandomGenerator import RandomGenerator
import json

class TestLevelDecryptor(unittest.TestCase):
    def setUp(self):
        self.random=RandomGenerator()
        self.random.seed(123)
        self.baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCb")
        self.levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCm")
        self.level=Level(self.baseMachine.getMachineSettings(),self.levelMachine.getMachineSettings())
        self.levelDecryptor=LevelDecryptor(self.baseMachine,self.levelMachine,self.level)
    def testDualOK(self):
        msg=[65,65,65,65,65]
        self.level.inputMsg=msg
        levelEncryptor=LevelEncryptor(self.baseMachine,self.levelMachine,self.level,self.random)
        self.random.seed(123)
        encLevel=levelEncryptor.encryptLevel()
        encLevel.inputMsg=""
        self.levelDecryptor.level=encLevel
        resultLevel=self.levelDecryptor.decryptLevel()
        self.assertEqual(resultLevel.inputMsg,msg)
        # print(resultLevel.toJson())

