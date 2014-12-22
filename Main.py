from ModernEnigma import ModernEnigma
from EnigmaDynamicFactory import EnigmaDynamicFactory
from Level import Level
from LevelEncryptor import LevelEncryptor
from LevelDecryptor import LevelDecryptor
from EnigmaConfigGenerator import EnigmaConfigGenerator
import json

baseMachineCfg=EnigmaConfigGenerator().createMachineConfig("MCb")
baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromConfig(baseMachineCfg)
baseMachine.adjustMachineSettings()

levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCm")
level=Level(baseMachine.getMachineSettings(),levelMachine.getMachineSettings())
levelMachine.adjustMachineSettings()

msg=[7,7,7,7,7]
level.inputMsg=msg
levelEncryptor=LevelEncryptor(baseMachine,levelMachine,level)
encLevel=levelEncryptor.encryptLevel()
encLevel.inputMsg=""
levelDecryptor=LevelDecryptor(baseMachine,levelMachine,level)
levelDecryptor.level=encLevel
resultLevel=levelDecryptor.decryptLevel()
# print(resultLevel.toJson())
print("MSG: ")
print(msg)
print("Enc: ")
print(encLevel.outputMsg)
print("Dec: ")
print(resultLevel.inputMsg)
