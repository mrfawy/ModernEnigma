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
        CharIndexMap.rangeTypeisCharacterBased=False
        seed=123
        self.baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCb")
        self.baseMachine.adjustMachineSettings()
        self.levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCm")
        self.levelMachine.adjustMachineSettings()
        self.level=Level(self.baseMachine.getMachineSettings(),self.levelMachine.getMachineSettings())
        self.levelDecryptor=LevelDecryptor(self.baseMachine,self.levelMachine,self.level)
    def testDualOK(self):
        # CharIndexMap.rangeTypeisCharacterBased=False
        # msg=[1,2,3,4,5]
        # self.level.inputMsg=msg
        # seed=123
        # levelEncryptor=LevelEncryptor(self.baseMachine,self.levelMachine,self.level,seed)
        # encLevel=levelEncryptor.encryptLevel()
        #
        # encLevel.inputMsg=""
        # self.levelDecryptor.level=encLevel
        # resultLevel=self.levelDecryptor.decryptLevel()
        #
        # self.assertEqual(resultLevel.inputMsg,msg)
        # print(resultLevel.toJson())
        raise("commented")

