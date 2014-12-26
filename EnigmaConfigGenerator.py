from CharIndexMap import CharIndexMap
from Util import Util
from RandomGenerator import RandomGenerator
from Shuffler import Shuffler

class EnigmaConfigGenerator(object):

    def __init__(self,seed=None):
        self.random=RandomGenerator(seed)
        self.shuffler=Shuffler(self.random)

        # self.CIPHER_ROTOR_COUNT_MIN=CharIndexMap.getRangeSize()//5
        # self.CIPHER_ROTOR_COUNT_MAX=CharIndexMap.getRangeSize()//2
        self.CIPHER_ROTOR_COUNT_MIN=5
        self.CIPHER_ROTOR_COUNT_MAX=10
        self.CIPHER_ROTOR_SIZE=CharIndexMap.getRangeSize()

        self.ROTOR_NOTCH_COUNT_MAX_RATIO=2 #will be divided

        # self.SWAP_ACTIVE_SIGNALS_COUNT_MIN=CharIndexMap.getRangeSize()//5
        # self.SWAP_ACTIVE_SIGNALS_COUNT_MAX=CharIndexMap.getRangeSize()//2
        self.SWAP_ACTIVE_SIGNALS_COUNT_MIN=CharIndexMap.getRangeSize()//5
        self.SWAP_ACTIVE_SIGNALS_COUNT_MAX=CharIndexMap.getRangeSize()//2

        # self.SWAP_ROTOR_L1_COUNT_MIN=CharIndexMap.getRangeSize()//5
        # self.SWAP_ROTOR_L1_COUNT_MAX=CharIndexMap.getRangeSize()//2
        self.SWAP_ROTOR_L1_COUNT_MIN=2
        self.SWAP_ROTOR_L1_COUNT_MAX=5
        self.SWAP_ROTOR_L1_MIN_SIZE=CharIndexMap.getRangeSize()
        self.SWAP_ROTOR_L1_MAX_SIZE=CharIndexMap.getRangeSize()

        # self.SWAP_ROTOR_L2_COUNT_MIN=CharIndexMap.getRangeSize()//5
        # self.SWAP_ROTOR_L2_COUNT_MAX=CharIndexMap.getRangeSize()//2
        self.SWAP_ROTOR_L2_COUNT_MIN=2
        self.SWAP_ROTOR_L2_COUNT_MAX=5
        self.SWAP_ROTOR_L2_MIN_SIZE=CharIndexMap.getRangeSize()
        self.SWAP_ROTOR_L2_MAX_SIZE=CharIndexMap.getRangeSize()

    def createMachineConfig(self,modelNo):
        seedStr=modelNo
        self.random.seed(seedStr)
        machineCfg={}
        machineCfg["CIPHER_MODULE"]=self.createCipherModuleConfig()
        machineCfg["SWAPPING_MODULE"]=self.createSwappingModuleConfig()
        return machineCfg

    def createCipherModuleConfig(self):
        moduleCfg={}
        moduleCfg["ROTOR_STOCK"]=self.createCipherRotorStockConfig()
        moduleCfg["REFLECTOR"]=self.createReflectorCfg()
        moduleCfg["PLUGBOARD"]=self.createPlugboardCfg()

        return moduleCfg

    def createSwappingModuleConfig(self):
        moduleCfg={}
        moduleCfg["L1_ROTOR_STOCK"]=self.createSwappingL1RotorStockConfig()
        moduleCfg["L2_ROTOR_STOCK"]=self.createSwappingL2RotorStockConfig()

        choosedL1Size=len(moduleCfg["L1_ROTOR_STOCK"][0]["wiring"])
        choosedL2Size=len(moduleCfg["L2_ROTOR_STOCK"][0]["wiring"])

        moduleCfg["L1_L2_MAPPER"]=self.createMapperCfg("L1L2MPPR",range(choosedL1Size),range(choosedL2Size))
        # moduleCfg["L2_CIPHER_MAPPER"]=self.createMapperCfg("L2CIPH_MPPR",range(choosedL2Size),range(cipherRotorsCount))
        return moduleCfg
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
        rotorConfig["wiring"]=self.createWiringCfg(range(size),range(size))
        if hasNotch:
            rotorConfig["notch"]=self.createNotchConfig(range(size))
        return rotorConfig

    def createNotchConfig(self,seq=None,count=None):
        if not seq:
            seq=CharIndexMap.getRange()
        if not count:
            count =self.random.nextInt(1,len(seq)//self.ROTOR_NOTCH_COUNT_MAX_RATIO)
        result=self.random.sample(seq,count)
        return result

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

    def getShuffledSequence(self,seq=None):
        if not seq:
            seq=CharIndexMap.getRange()
        shuffler=Shuffler(self.random)
        shSeq= shuffler.shuffleSeq(seq)
        return shSeq


    def createReflectorCfg(self,id="RFLCTR",seq=None):
        if not seq:
            seq=CharIndexMap.getRange()
        reflectorConfig={"ID":id}
        reflectorConfig["wiring"]=self.getValidReflectorShuffledWiringCfg(seq)
        return reflectorConfig

    def getValidReflectorShuffledWiringCfg(self,sequence=None):
        if not sequence:
            sequence=CharIndexMap.getRange()
        wiringTuples=[]
        seq=self.shuffler.shuffleSeq(sequence)
        while len(seq)>0:
            selectedPair=self.random.sample(seq,2)
            wiringTuples.append((selectedPair[0],selectedPair[1]))
            wiringTuples.append((selectedPair[1],selectedPair[0]))
            seq.remove(selectedPair[0])
            seq.remove(selectedPair[1])
        result=Util.convertTupleListToMap(wiringTuples)

        return result

    def createPlugboardCfg(self,id="PLGBRD",seq=None):
        if not seq:
            seq=CharIndexMap.getRange()
        plugboardConfig={"ID":id}
        plugboardConfig["wiring"]=self.getValidReflectorShuffledWiringCfg(seq)
        return plugboardConfig

    def createMapperCfg(self,id,fromRange,toRange):
        mapperCfg={"ID":str(id)}
        mapperCfg["wiring"]=self.createWiringCfg(fromRange,toRange)
        return mapperCfg


    def createWiringCfg(self,fromRange,toRange):
        wiringTuples=[]
        if fromRange==toRange:
            shuffledToSeq=self.getShuffledSequence(toRange)
            for i in range(0,len(fromRange)):
                    wiringTuples.append((fromRange[i],shuffledToSeq[i]))
        else:
            coveredTo=[]
            for fromIndex in fromRange:
                mappedTo=self.random.sample(toRange,self.random.nextInt(1,len(toRange)))
                for m in mappedTo:
                    wiringTuples.append((fromIndex,m))
                    if m not in coveredTo:
                        coveredTo.append(m)
            for toIndex in toRange:
                if toIndex not in coveredTo:
                    mappedFrom=self.random.sample(fromRange,self.random.nextInt(1,len(fromRange)))
                    for m in mappedFrom:
                        wiringTuples.append((m,toIndex))

        wiringCfg=Util.convertTupleListToMap(wiringTuples)
        return wiringCfg

