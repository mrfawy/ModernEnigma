from ModernEnigma import ModernEnigma
from CharIndexMap import CharIndexMap
from Wiring import Wiring
from Rotor import Rotor
from SwappingSwitch import SwappingSwitch
from Reflector import Reflector
from Plugboard import PlugBoard
import random
class EnigmaDynamicFactory(object):
    ROTOR_COUNT_MIN=1
    ROTOR_COUNT_MAX=1


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

        """swapping mechanism"""
        machineConfig["SWAPPING"]={}
        swappingConf=machineConfig["SWAPPING"]
        swappingConf["L1ROTORS"]=[]
        swappingConf["L2ROTORS"]=[]

        fixedActiveSwapSingals=self.nextInt(1,CharIndexMap.getRangeSize()//4)
        swappingConf["FIXED_SWAP_SIGNALS"]=self.getShuffledSequence()[0:fixedActiveSwapSingals]

        l1swapRotorCount=self.nextInt(CharIndexMap.getRangeSize()//5,CharIndexMap.getRangeSize()//2)
        for i in range(l1swapRotorCount):
            l1RotorConfig=self.createRotorConfig(i) #level 1 is normal rotor size
            swappingConf["L1ROTORS"].append(l1RotorConfig)

        l2swapRotorCount=self.nextInt(CharIndexMap.getRangeSize()//5,CharIndexMap.getRangeSize()//2)
        l2RotorSize=self.nextInt(CharIndexMap.getRangeSize()//3,2*CharIndexMap.getRangeSize()//3) # between 1/3 , 2/3
        for i in range(l2swapRotorCount):
            l2RotorConfig=self.createSwappingLevel2RotorConfig(i,l2RotorSize)
            swappingConf["L2ROTORS"].append(l2RotorConfig)


        swappingConf["L1_L2_SEPARATOR"]=self.createSwappingSeparatorConfig("L1_SEP_L2",l2RotorSize)
        swappingConf["L2_CIPHER_MAPPER"]=self.createSwappingSeparatorConfig("L2_SEP_CIPH",rotorCount,l2RotorSize)

        return machineConfig

    def createEnigmaMachineFromConfig(self,config):
        rotorCfgList=config["ROTORS"]
        rotorStockList=[]
        for r in rotorCfgList:
            rotorStockList.append(Rotor(r["ID"],Wiring(r["wiring"]),r["notch"]))
        plugboard=PlugBoard(Wiring(config["PLUGBOARD"]["wiring"]))
        reflector=Reflector(Wiring(config["REFLECTOR"]["wiring"]))

        "Swapping mechanism"
        swapCfg=config["SWAPPING"]
        l1rotorCfgList=swapCfg["L1ROTORS"]
        l2rotorCfgList=swapCfg["L2ROTORS"]
        l1l2SeparatorCfg=swapCfg["L1_L2_SEPARATOR"]
        l2CiphSeparatorCfg=swapCfg["L2_CIPHER_MAPPER"]

        l1SwappingRotorStockList=[]
        for l1r in l1rotorCfgList:
            l1SwappingRotorStockList.append(Rotor(l1r["ID"],Wiring(l1r["wiring"]),l1r["notch"]))


        l2SwappingRotorStockList=[]
        for l2r in l2rotorCfgList:
            l2SwappingRotorStockList.append(Rotor(l2r["ID"],Wiring(l2r["wiring"]),l2r["notch"],len(l2r["wiring"])))


        l1l2SeparatorSwitch=self.createSwappingSeparator(l1l2SeparatorCfg)
        l2CipherMapper=self.createSwappingSeparator(l2CiphSeparatorCfg)
        fixedSwapSignals=swapCfg["FIXED_SWAP_SIGNALS"]

        mc=ModernEnigma(rotorStockList,reflector,plugboard,fixedSwapSignals,l1SwappingRotorStockList,l2SwappingRotorStockList,l1l2SeparatorSwitch,l2CipherMapper)
        return mc

    def createReflectorConfig(self,id):
        reflectorConfig={"ID":id}
        reflectorConfig["wiring"]=self.seqToStr(self.getValidReflectorShuffledSequence())
        return reflectorConfig

    def getValidReflectorShuffledSequence(self):
        result=[]
        #init result before mapping
        for i in range(CharIndexMap.getRangeSize()):
            result.append("")

        seq= self.getShuffledSequence()
        while len(seq)>0:
            selectedPair=random.sample(seq,2)
            result[CharIndexMap.charToIndex(selectedPair[0])]=selectedPair[1]
            result[CharIndexMap.charToIndex(selectedPair[1])]=selectedPair[0]
            seq.remove(selectedPair[0])
            seq.remove(selectedPair[1])

        return result


    def createRotorConfig(self,id):
        rotorConfig={"ID":id}
        rotorConfig["wiring"]=self.seqToStr(self.getShuffledSequence())
        rotorConfig["notch"]=self.seqToStr(self.getSampleNotchSeq())
        return rotorConfig

    def createSwappingLevel2RotorConfig(self,id,size):
        rotorConfig={"ID":id}
        seqToShuffle=[]
        for i in range(size):
            seqToShuffle.append(CharIndexMap.indexToChar(i))

        rotorConfig["wiring"]=self.seqToStr(self.getShuffledSequence(seqToShuffle))
        rotorConfig["notch"]=self.seqToStr(self.getSampleNotchSeq(seqToShuffle))
        return rotorConfig
    def createSwappingSeparatorConfig(self,id,toSize,fromSize=CharIndexMap.getRangeSize()):
        rotorConfig={"ID":id}
        fromIndexRange=range(fromSize)
        toIndexRange=range(toSize)
        mappingTuples=[]
        coveredTo=[]
        for fromIndex in fromIndexRange:
            mappedTo=random.sample(toIndexRange,self.nextInt(1,len(toIndexRange)))
            for m in mappedTo:
                mappingTuples.append((fromIndex,m))
                coveredTo.append(m)
        for toIndex in toIndexRange:
            if toIndex not in coveredTo:
                mappedFrom=random.sample(fromIndexRange,self.nextInt(1,len(fromIndexRange)))
                for m in mappedFrom:
                    mappingTuples.append((m,toIndex))
        rotorConfig["wiring"]={}
        wiringCfg=rotorConfig["wiring"]
        for t in mappingTuples:
            fromPin=t[0]
            toPin=t[1]
            if fromPin not in wiringCfg:
                wiringCfg[fromPin]=[]
            wiringCfg[fromPin].append(toPin)
        return rotorConfig

    def createSwappingSeparator(self,config):
        w=Wiring()
        mappingTuples=[]
        for fromPin,value in config["wiring"].items():
            for toPin in value:
                mappingTuples.append((fromPin,toPin))

        w.initWiringFromTupleList(mappingTuples)

        return SwappingSwitch(w)






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
    def getSampleNotchSeq(self,seq=CharIndexMap.getRange()):
        result=random.sample(seq,self.nextInt(0,len(seq)//2))
        return result


def mainTst():
    mc1=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCx")
    msg="AAAAAAA"
    print("MSG:"+msg)
    encMsg=""
    for c in msg:
        encMsg+=mc1.processKeyPress(c)
    print ("Encrpyted:"+encMsg)

    mc2=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCx")
    decMsg=""
    for c in encMsg:
        decMsg+=mc2.processKeyPress(c)

    print("Decrypted:"+decMsg)

    print("settings:"+mc1.getMachineSettings())
def machineFromStgTst():
    stg="232221201918171615141312111009080706050403020100|AAAAAAAAAAAAAAAAAAAAACDO|"
    mc1=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCx")
    mc1.adjustMachineSettings(stg)
    mc2=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCx")
    mc2.adjustMachineSettings(stg)
    msg="AAAAAAAAAAAAAAAAAAAAAA"
    print("MSG:"+msg)
    encMsg=""
    for c in msg:
        encMsg+=mc1.processKeyPress(c)
    print ("Encrpyted:"+encMsg)
    decMsg=""
    for c in encMsg:
        decMsg+=mc2.processKeyPress(c)
    print("Decrypted:"+decMsg)
    print("settings:"+mc1.getMachineSettings())

# machineFromStgTst()
