from ModernEnigma import ModernEnigma
from EnigmaDynamicFactory import EnigmaDynamicFactory
from Level import Level
from LevelEncryptor import LevelEncryptor
from LevelDecryptor import LevelDecryptor


baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCb")
levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCm")
level=Level(baseMachine.getMachineSettings(),levelMachine.getMachineSettings())
msg="987123"
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
