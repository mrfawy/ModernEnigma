from ModernEnigma import ModernEnigma
from EnigmaDynamicFactory import EnigmaDynamicFactory
from Level import Level
from LevelEncryptor import LevelEncryptor
from LevelDecryptor import LevelDecryptor
from EnigmaConfigGenerator import EnigmaConfigGenerator
from RandomGenerator import RandomGenerator
import json

baseMachineCfg=EnigmaConfigGenerator(RandomGenerator(123)).createMachineConfig("MCb")
baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromConfig(baseMachineCfg)
baseMachine.adjustMachineSettings()

levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCm")
levelMachine.adjustMachineSettings()
level=Level(baseMachine.getMachineSettings(),levelMachine.getMachineSettings())

msg=[2,2,2,2,2]
level.inputMsg=msg

levelEncryptor=LevelEncryptor(baseMachine,levelMachine,level,RandomGenerator(123))
encLevel=levelEncryptor.encryptLevel()

encLevel.inputMsg=""
baseMachineCfg=EnigmaConfigGenerator(RandomGenerator(123)).createMachineConfig("MCb")
baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromConfig(baseMachineCfg)
baseMachine.adjustMachineSettings()

levelDecryptor=LevelDecryptor(baseMachine,levelMachine,level)
levelDecryptor.level=encLevel
resultLevel=levelDecryptor.decryptLevel()
print("MSG: ")
print(msg)
print("Enc: ")
print(encLevel.outputMsg)
print("Dec: ")
print(resultLevel.inputMsg)
