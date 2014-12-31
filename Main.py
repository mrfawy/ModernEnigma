from ModernEnigma import ModernEnigma
from EnigmaDynamicFactory import EnigmaDynamicFactory
from Level import Level
from LevelEncryptor import LevelEncryptor
from LevelDecryptor import LevelDecryptor
from EnigmaConfigGenerator import EnigmaConfigGenerator
from RandomGenerator import RandomGenerator
from FileReader import FileReader
from CharIndexMap import CharIndexMap
from Util import Util
from StreamConverter import CharacterStreamConverter
import json
import codecs
import time

def encryptFile():
    CharIndexMap.rangeTypeisCharacterBased=False
    start_time = time.time()

    baseMachineCfg=EnigmaConfigGenerator(RandomGenerator(123)).createMachineConfig("MCb")
    baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromConfig(baseMachineCfg)
    baseMachine.adjustMachineSettings()

    levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCm")
    levelMachine.adjustMachineSettings()
    level=Level(baseMachine.getMachineSettings(),levelMachine.getMachineSettings())

    elapsed_time = time.time() - start_time
    print("2 MAchines were created in :"+str(elapsed_time))

    start_time = time.time()
    msg=FileReader().readSeqFromFile("tst.txt")
    elapsed_time = time.time() - start_time
    print("Parsed File to read Seq in : "+str(elapsed_time))
    level.inputMsg=msg


    start_time = time.time()
    levelEncryptor=LevelEncryptor(baseMachine,levelMachine,level,RandomGenerator(123))
    encLevel=levelEncryptor.encryptLevel()
    elapsed_time = time.time() - start_time
    print("Encrypted Seq in : "+str(elapsed_time))

    FileReader().writeSeqTofile(encLevel.outputMsg,"tst.enc",True)
    print("Encrypted File written")

    encLevel.inputMsg=""

    start_time = time.time()
    levelDecryptor=LevelDecryptor(baseMachine,levelMachine,level)
    levelDecryptor.level=encLevel
    resultLevel=levelDecryptor.decryptLevel()
    elapsed_time = time.time() - start_time
    print("Decrypted Sequence in :"+str(elapsed_time))

    FileReader().writeSeqTofile(resultLevel.inputMsg,"tst.dec",False)
    print("Decrypted File written")

    print("DONE !!")

def encryptTextAsBin():
    CharIndexMap.rangeTypeisCharacterBased=False

    start_time = time.time()

    baseMachineCfg=EnigmaConfigGenerator(RandomGenerator(123)).createMachineConfig("MCb")
    baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromConfig(baseMachineCfg)
    baseMachine.adjustMachineSettings()

    levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCm")
    levelMachine.adjustMachineSettings()

    level=Level(baseMachine.getMachineSettings(),levelMachine.getMachineSettings())

    elapsed_time = time.time() - start_time
    print("2 MAchines were created in :"+str(elapsed_time))

    msg="Hello Enigma !"
    msgSeq=Util.encodeStringIntoByteList(msg)
    level.inputMsg=msgSeq


    start_time = time.time()
    levelEncryptor=LevelEncryptor(baseMachine,levelMachine,level,RandomGenerator(123))
    encLevel=levelEncryptor.encryptLevel()
    elapsed_time = time.time() - start_time
    print("Encrypted Seq in : "+str(elapsed_time))
    print("ENC:")
    print(Util.convertByteListIntoHexString(encLevel.outputMsg))

    encLevel.inputMsg=""

    start_time = time.time()
    levelDecryptor=LevelDecryptor(baseMachine,levelMachine,level)
    levelDecryptor.level=encLevel
    resultLevel=levelDecryptor.decryptLevel()
    elapsed_time = time.time() - start_time
    print("Decrypted Sequence in :"+str(elapsed_time))
    print("DEC:")
    print(resultLevel.inputMsg)
    print(Util.decodeByteListIntoString(resultLevel.inputMsg))


    print("DONE !!")
encryptTextAsBin()
