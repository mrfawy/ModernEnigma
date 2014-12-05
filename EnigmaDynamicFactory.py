from ModernEnigma import ModernEnigma
from CharIndexMap import CharIndexMap
import random
class EnigmaDynamicFactory(object):
    ROTORS="ROTORS"
    REFLECTOR="REFLECTOR"
    PLUGBOARD="PLUGBOARD"

    def __init__(self,machineModel):
        seedStr=machineModel
        random.seed(seedStr)
        self.machineConfig=None

    def createMachineConfig(self):
        self.machineConfig={"ROTORS":[]}
        rotorCount=self.nextInt(CharIndexMap.getRangeSize()//5,CharIndexMap.getRangeSize()//2)
        for i in range(rotorCount):
            rotorConfig=self.createRotorConfig(i)
            self.machineConfig["ROTORS"].append(rotorConfig)
        self.machineConfig["REFLECTOR"]=self.createReflectorConfig(self.nextInt())
        self.machineConfig["PLUGBOARD"]=self.createPlugboardConfig(self.nextInt())
        return self.machineConfig

    def createEnigmaMachineFromConfig(self,config):
        rotorCfgList=confg[ROTORS]
        rotorList=[]
        for r in rotorCfgList:
            rotorList.append(r["ID"],Wiring(r["wiring"]),r["noch"])
        plugboard=PlugBoard(confg[PLUGBOARD]["wiring"])
        reflector=Reflector(confg[REFLECTOR]["wiring"])
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

f=EnigmaDynamicFactory("1")
print(f.createEnigmaMachine())
