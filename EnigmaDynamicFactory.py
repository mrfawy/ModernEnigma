from ModernEnigma import ModernEnigma
from CharIndexMap import CharIndexMap
from Wiring import Wiring
from Rotor import Rotor
from Reflector import Reflector
from Plugboard import PlugBoard
import random
class EnigmaDynamicFactory(object):

    def __init__(self):
        pass

    def createEnigmaMachineFromModel(self,modelNo):
        cfg=self.createMachineConfig(modelNo)
        mc=self.createEnigmaMachineFromConfig(cfg)
        return mc

    def createMachineConfig(self,modelNo):
        seedStr=modelNo
        random.seed(seedStr)
        machineConfig={"ROTORS":[]}
        rotorCount=self.nextInt(CharIndexMap.getRangeSize()//5,CharIndexMap.getRangeSize()//2)
        for i in range(rotorCount):
            rotorConfig=self.createRotorConfig(i)
            machineConfig["ROTORS"].append(rotorConfig)
        machineConfig["REFLECTOR"]=self.createReflectorConfig(self.nextInt())
        machineConfig["PLUGBOARD"]=self.createPlugboardConfig(self.nextInt())
        return machineConfig

    def createEnigmaMachineFromConfig(self,config):
        rotorCfgList=config["ROTORS"]
        rotorList=[]
        for r in rotorCfgList:
            rotorList.append(Rotor(r["ID"],Wiring(r["wiring"]),r["noch"]))
        plugboard=PlugBoard(Wiring(config["PLUGBOARD"]["wiring"]))
        reflector=Reflector(Wiring(config["REFLECTOR"]["wiring"]))
        mc=ModernEnigma(rotorList,reflector,plugboard)
        return mc

    def createReflectorConfig(self,id):
        reflectorConfig={"ID":id}
        reflectorConfig["wiring"]=self.seqToStr(self.getShuffledSequence())
        return reflectorConfig

    def createRotorConfig(self,id):
        rotorConfig={"ID":id}
        rotorConfig["wiring"]=self.seqToStr(self.getShuffledSequence())
        rotorConfig["noch"]=self.seqToStr(self.getSampleSeq())
        return rotorConfig

    def createPlugboardConfig(self,id):
        plugboardConfig={"ID":id}
        plugboardConfig["wiring"]=self.seqToStr(CharIndexMap.getRange())
        return plugboardConfig

    def seqToStr(self,seq):
        result=""
        for item in seq:
            result+=item
        return result



    def nextInt(self,a=0,b=CharIndexMap.getRangeSize()):
        return random.randint(a,b)
    def getShuffledSequence(self,seq=CharIndexMap.getRange()):
        result=seq
        times=self.nextInt()
        for t in range(times):
            #to keep the original and copy it
            result= sorted(result, key=lambda k: random.random())
        return result
    def getSampleSeq(self,seq=CharIndexMap.getRange()):
        result=random.sample(seq,self.nextInt(0,CharIndexMap.getRangeSize()//2))
        return result

mcCfg=EnigmaDynamicFactory().createMachineConfig("1")
mc1=EnigmaDynamicFactory().createEnigmaMachineFromConfig(mcCfg)
msg="AAAAAAA"
print("MSG:"+msg)
encMsg=""
for c in msg:
    encMsg+=mc1.processKeyPress(c)
print ("Encrpyted:"+encMsg)

mc2=EnigmaDynamicFactory().createEnigmaMachineFromConfig(mcCfg)
decMsg=""
for c in encMsg:
    decMsg+=mc2.processKeyPress(c)

print("Decrypted:"+decMsg)


