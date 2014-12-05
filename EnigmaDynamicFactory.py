from ModernEnigma import ModernEnigma
from CharIndexMap import CharIndexMap
import random
class EnigmaDynamicFactory(object):
    def __init__(self,machineModel):
        seedStr=machineModel
        random.seed(seedStr)
        self.machineConfig={"ROTORS":[]}


    def createEnigmaMachine(self):
        rotorCount=self.nextInt()
        for i in range(rotorCount):
            rotorConfig=self.createRotorConfig(i)
            self.machineConfig["ROTORS"].append(rotorConfig)
        self.machineConfig["REFLECTOR"]=self.createReflectorConfig()
        self.machineConfig["PLUGBOARD"]=None
        return self.machineConfig

    def createReflectorConfig(self):
        reflectorConfig={}
        reflectorConfig["wiring"]=self.seqToStr(self.getShuffledSequence())
        return reflectorConfig

    def createRotorConfig(self,id):
        rotorConfig={"ID":id}
        rotorConfig["wiring"]=self.seqToStr(self.getShuffledSequence())
        rotorConfig["noch"]=self.seqToStr(self.getSampleSeq())
        return rotorConfig

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
        result=random.sample(seq,self.nextInt(0,CharIndexMap.getRangeSize()/2))
        return result

f=EnigmaDynamicFactory("1")
print(f.createEnigmaMachine())
