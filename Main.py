from ModernEnigma import ModernEnigma
from EnigmaDynamicFactory import EnigmaDynamicFactory
from Level import Level
from LevelEncryptor import LevelEncryptor
from LevelDecryptor import LevelDecryptor
import json

baseMachineCfg=EnigmaDynamicFactory().createMachineConfig("MCb")
baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromConfig(baseMachineCfg)
levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCm")
level=Level(baseMachine.getMachineSettings(),levelMachine.getMachineSettings())
msg="HELLOXENIGMA!"
level.inputMsg=msg.upper()
levelEncryptor=LevelEncryptor(baseMachine,levelMachine,level)
encLevel=levelEncryptor.encryptLevel()
encLevel.inputMsg=""
levelDecryptor=LevelDecryptor(baseMachine,levelMachine,level)
levelDecryptor.level=encLevel
resultLevel=levelDecryptor.decryptLevel()
print(resultLevel.toJson())
print("MSG: "+msg)
print("Enc: "+encLevel.outputMsg)
print("Dec: "+resultLevel.inputMsg)
