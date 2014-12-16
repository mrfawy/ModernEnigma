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
        ENC="""U//=27%"L+Z<<+VO!<3=K/][?XG"=<"&]P"":QP7XZ.#6="""
        self.assertEqual(resultLevel.outputMsg,ENC)
        # print(resultLevel.toJson())

