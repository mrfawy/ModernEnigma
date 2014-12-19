from ModernEnigma import ModernEnigma
from CharIndexMap import CharIndexMap
from Wiring import Wiring
from Rotor import Rotor
from SwappingSwitch import SwappingSwitch
from Reflector import Reflector
from Plugboard import PlugBoard
from Util import Util
from RandomGenerator import RandomGenerator
class EnigmaDynamicFactory(object):


    def __init__(self,seed=None):
        self.random=RandomGenerator(seed)

        self.CIPHER_ROTOR_COUNT_MIN=CharIndexMap.getRangeSize()//5
        self.CIPHER_ROTOR_COUNT_MAX=CharIndexMap.getRangeSize()//2
        self.CIPHER_ROTOR_SIZE=CharIndexMap.getRangeSize()

        self.ROTOR_NOTCH_COUNT_MIN=1
        self.ROTOR_NOTCH_COUNT_MAX=1

        self.SWAP_ACTIVE_SIGNALS_COUNT_MIN=1
        self.SWAP_ACTIVE_SIGNALS_COUNT_MAX=1

        self.SWAP_ROTOR_L1_COUNT_MIN=CharIndexMap.getRangeSize()//5
        self.SWAP_ROTOR_L1_COUNT_MAX=CharIndexMap.getRangeSize()//2
        self.SWAP_ROTOR_L1_MIN_SIZE=CharIndexMap.getRangeSize()
        self.SWAP_ROTOR_L1_MAX_SIZE=CharIndexMap.getRangeSize()

        self.SWAP_ROTOR_L2_COUNT_MIN=CharIndexMap.getRangeSize()//5
        self.SWAP_ROTOR_L2_COUNT_MAX=CharIndexMap.getRangeSize()//2
        self.SWAP_ROTOR_L2_MIN_SIZE=CharIndexMap.getRangeSize()
        self.SWAP_ROTOR_L2_MAX_SIZE=CharIndexMap.getRangeSize()
        pass

    def createEnigmaMachineFromModel(self,modelNo):
        cfg=self.createMachineConfig(modelNo)
        mc=self.createEnigmaMachineFromConfig(cfg)
        return mc

    def createRotorStockConfig(self,rotorCount,rotorSize):
        rotorStock=[]
        for i in range(rotorCount):
            rotorConfig=self.createRotorConfig(i,rotorSize)
            rotorStock.append(rotorConfig)
        return rotorStock

    def createRotorConfig(self,id,size=None,hasNotch=True):
        if not size:
            size=CharIndexMap.getRangeSize()
        rotorConfig={"ID":id}
        rotorConfig["wiring"]=self.createWiringCfg(CharIndexMap.getRange(),CharIndexMap.getRange())
        if hasNotch:
            rotorConfig["notch"]=Util.seqToStr(self.getSampleNotchSeq(seqToShuffle))
        return rotorConfig

    def createCipherRotorStockConfig(self,rotorCount=None):
        if not rotorCount:
            rotorCount=self.random.nextInt(self.CIPHER_ROTOR_COUNT_MIN,self.CIPHER_ROTOR_COUNT_MAX)

        rotorSize=CharIndexMap.getRangeSize()
        return self.createRotorStockConfig(rotorCount,rotorSize)

    def createSwappingL1RotorStockConfig(self,rotorCount=None):
        if not rotorCount:
            rotorCount=self.random.nextInt(self.SWAP_ROTOR_L1_COUNT_MIN,self.SWAP_ROTOR_L1_COUNT_MAX)

        rotorsize=self.random.nextInt(self.SWAP_ROTOR_L1_MIN_SIZE,self.SWAP_ROTOR_L1_MAX_SIZE)

        return self.createRotorStockConfig(rotorCount,rotorsize)

    def createSwappingL2RotorStockConfig(self,rotorCount=None):
        if not rotorCount:
            rotorCount=self.random.nextInt(self.SWAP_ROTOR_L2_COUNT_MIN,self.SWAP_ROTOR_L2_COUNT_MAX)

        rotorsize=self.random.nextInt(self.SWAP_ROTOR_L2_MIN_SIZE,self.SWAP_ROTOR_L2_MAX_SIZE)

        return self.createRotorStockConfig(rotorCount,rotorsize)
    def createActiveSwapSignalsConfig(self,id="ACTV",count=None):
        if not count:
            count=self.random.nextInt(self.SWAP_ACTIVE_SIGNALS_COUNT_MIN,self.SWAP_ROTOR_L1_COUNT_MAX)
        activeSwapCfg={}
        activeSwapCfg["ID"]=id
        activeSwapCfg["SIGNALS"]=self.getShuffledSequence()[0:count]

        return activeSwapCfg


    def createCipherModuleConfig(self):
        moduleCfg={}
        moduleCfg["ROTOR_STOCK"]=self.createCipherRotorStockConfig()
        moduleCfg["REFLECTOR"]=self.createReflectorConfig()
        moduleCfg["PLUGBOARD"]=self.createPlugboardConfig()

        return moduleCfg

    def createSwappingModuleConfig(self):
        moduleCfg={}
        moduleCfg["L1_ROTOR_STOCK"]=self.createSwappingL1RotorStockConfig()
        moduleCfg["L2_ROTOR_STOCK"]=self.createSwappingL2RotorStockConfig()
        moduleCfg["ACTIVE_SWAP_SIGNALS"]=self.createActiveSwapSignalsConfig()


    def createMachineConfig(self,modelNo):
        seedStr=modelNo
        self.random.seed(seedStr)
        machineConfg={}
        machineConfg["CIPHER_MODULE"]=self.createCipherModuleConfig()
        machineConfg["SWAPPING_MODULE"]=self.createSwappingModuleConfig()

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

    def createReflectorConfig(self,id="RFLCTR"):
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

    def createWiringCfg(self,fromRange,toRange):
        wiringTuples=[]
        if fromRange==toRange:
            shuffledToSeq=self.shuffler.shuffleSeq(toRange)
            for f in fromRange:
                for st in shuffledToSeq:
                    wiringTuples.append((f,st))
        else:
            for fromIndex in fromRange:
                mappedTo=self.random.sample(toIndexRange,self.nextInt(1,len(toIndexRange)))
                for m in mappedTo:
                    mappingTuples.append((fromIndex,m))
                    coveredTo.append(m)
            for toIndex in toRange:
                if toIndex not in coveredTo:
                    mappedFrom=self.random.sample(fromIndexRange,self.nextInt(1,len(fromIndexRange)))
                    for m in mappedFrom:
                        mappingTuples.append((m,toIndex))

        wiringCfg={}
        for t in mappingTuples:
            fromPin=t[0]
            toPin=t[1]
            if fromPin not in wiringCfg:
                wiringCfg[fromPin]=[]
            wiringCfg[fromPin].append(toPin)
        return wiringCfg

    def createSwappingSeparator(self,config):
        w=Wiring()
        mappingTuples=[]
        for fromPin,value in config["wiring"].items():
            for toPin in value:
                mappingTuples.append((fromPin,toPin))

        w.initWiringFromTupleList(mappingTuples)

        return SwappingSwitch(w)

    def createPlugboardConfig(self,id="PLGBRD"):
        plugboardConfig={"ID":id}
        plugboardConfig["wiring"]=self.createWiringCfg(CharIndexMap.getRange(),CharIndexMap.getRange())
        return plugboardConfig

    def createNotchConfig(self,seq=CharIndexMap.getRange(),count=None):
        if not count:
            count =self.random.nextInt(self.ROTOR_NOTCH_COUNT_MIN,self.ROTOR_NOTCH_COUNT_MAX)
        result=self.random.sample(seq,self.nextInt(0,len(seq)//2))
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
