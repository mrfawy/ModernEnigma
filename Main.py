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
from MachineSettingManager import MachineSettingManager
from MachineSettingsMemento import MachineSettingsMemento
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
    seed=None

    baseMachineModelName=EnigmaConfigGenerator(seed).createRandomModelName()
    baseMachineCfg=EnigmaConfigGenerator(seed).createMachineConfig(baseMachineModelName)

    Util.writeObjectToFileAsJson(baseMachineCfg,"./state/baseMcCfg.json")

    baseMachine=EnigmaDynamicFactory(seed).createEnigmaMachineFromConfig(baseMachineCfg)
    baseMcStg=MachineSettingManager(seed).generateRandomSettingsForMachine(baseMachine)

    Util.writeObjectToFileAsJson(baseMcStg.getAsMap(),"./state/baseMcStg.json")

    baseMachine.adjustMachineSettings(baseMcStg)

    levelMachineModelName=EnigmaConfigGenerator(seed).createRandomModelName()
    levelMcCfg=EnigmaConfigGenerator(seed).createMachineConfig(levelMachineModelName)
    Util.writeObjectToFileAsJson(levelMcCfg,"./state/levelMcCfg.json")
    levelMachine=EnigmaDynamicFactory(seed).createEnigmaMachineFromConfig(levelMcCfg)
    levelMcStg=MachineSettingManager(seed).generateRandomSettingsForMachine(levelMachine)
    Util.writeObjectToFileAsJson(levelMcStg.getAsMap(),"./state/levelMcStg.json")
    levelMachine.adjustMachineSettings(levelMcStg)

    level=Level(baseMcStg,levelMcStg,seed)


    Util.writeObjectToFileAsJson(level.getAsMap(),"./state/level.json")


    elapsed_time = time.time() - start_time
    # print("2 MAchines were created in :"+str(elapsed_time))

    msg="Hello Enigma !"
    msgSeq=Util.encodeStringIntoByteList(msg)
    level.inputMsg=msgSeq


    start_time = time.time()
    levelEncryptor=LevelEncryptor(baseMachine,levelMachine,level,seed)
    encLevel=levelEncryptor.encryptLevel()
    elapsed_time = time.time() - start_time
    # print("Encrypted Seq in : "+str(elapsed_time))
    # print("ENC:")
    # print(Util.convertByteListIntoHexString(encLevel.outputMsg))

    encLevel.inputMsg=""

    start_time = time.time()
    levelDecryptor=LevelDecryptor(baseMachine,levelMachine,level)
    levelDecryptor.level=encLevel
    resultLevel=levelDecryptor.decryptLevel()
    elapsed_time = time.time() - start_time
    # print("Decrypted Sequence in :"+str(elapsed_time))
    print("DEC:")
    print(resultLevel.inputMsg)
    # print(Util.decodeByteListIntoString(resultLevel.inputMsg))

    print("DONE !!")
    return resultLevel.inputMsg

def runTillError():
    for i in range(100):
        res=encryptTextAsBin()
        expected=[72, 101, 108, 108, 111, 32, 69, 110, 105, 103, 109, 97, 32, 33]
        if len(res)==0 or res!=expected:
            return
    print(" ALL CASES DONE !!")
def loadFromJsonFiles():
    CharIndexMap.rangeTypeisCharacterBased=False
    seed=None
    baseMcCfg=Util.readJsonFileIntoObject("./state/baseMcCfg.json")
    baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromConfig(baseMcCfg)
    baseMcStg=MachineSettingsMemento.loadFromMap(Util.readJsonFileIntoObject("./state/baseMcStg.json"))
    baseMachine.adjustMachineSettings(baseMcStg)

    levelMcCfg=Util.readJsonFileIntoObject("./state/levelMcCfg.json")
    levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromConfig(levelMcCfg)
    levelMcStg=MachineSettingsMemento.loadFromMap(Util.readJsonFileIntoObject("./state/levelMcStg.json"))
    levelMachine.adjustMachineSettings(levelMcStg)

    level=Level.loadFromMap(Util.readJsonFileIntoObject("./state/level.json"))

    msg="Hello Enigma !"
    msgSeq=Util.encodeStringIntoByteList(msg)
    level.inputMsg=msgSeq
    levelEncryptor=LevelEncryptor(baseMachine,levelMachine,level,seed)
    encLevel=levelEncryptor.encryptLevel()

    print("ENC:")
    print(Util.convertByteListIntoHexString(encLevel.outputMsg))

    encLevel.inputMsg=""

    levelDecryptor=LevelDecryptor(baseMachine,levelMachine,level)
    levelDecryptor.level=encLevel
    resultLevel=levelDecryptor.decryptLevel()
    print("DEC:")
    print(resultLevel.inputMsg)
    print(Util.decodeByteListIntoString(resultLevel.inputMsg))

    print("DONE !!")
    return resultLevel.inputMsg
    pass

# runTillError()
loadFromJsonFiles()
