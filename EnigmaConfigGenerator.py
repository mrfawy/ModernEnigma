from CharIndexMap import CharIndexMap
from Util import Util
from RandomGenerator import RandomGenerator
from Shuffler import Shuffler
import hashlib

class EnigmaConfigGenerator(object):

    def __init__(self,seed=None):
        self.random=RandomGenerator(seed)
        self.shuffler=Shuffler(self.random)

        # self.CIPHER_ROTOR_COUNT_MIN=CharIndexMap.getRangeSize()//5
        # self.CIPHER_ROTOR_COUNT_MAX=CharIndexMap.getRangeSize()//2
        self.CIPHER_ROTOR_COUNT_MIN=2
        self.CIPHER_ROTOR_COUNT_MAX=3
        self.CIPHER_ROTOR_SIZE=CharIndexMap.getRangeSize()

        self.ROTOR_NOTCH_COUNT_MAX_RATIO=2 #will be divided

        self.SWAP_ACTIVE_SIGNALS_COUNT_MIN=2
        self.SWAP_ACTIVE_SIGNALS_COUNT_MAX=3
        # self.SWAP_ACTIVE_SIGNALS_COUNT_MIN=CharIndexMap.getRangeSize()//5
        # self.SWAP_ACTIVE_SIGNALS_COUNT_MAX=CharIndexMap.getRangeSize()//2

        # self.SWAP_ROTOR_COUNT_MIN=CharIndexMap.getRangeSize()//5
        # self.SWAP_ROTOR_COUNT_MAX=CharIndexMap.getRangeSize()//2
        self.SWAP_ROTOR_COUNT_MIN=2
        self.SWAP_ROTOR_COUNT_MAX=2
        # self.SWAP_ROTOR_MIN_SIZE=CharIndexMap.getRangeSize()
        # self.SWAP_ROTOR_MAX_SIZE=CharIndexMap.getRangeSize()
        self.SWAP_ROTOR_MIN_SIZE=5
        self.SWAP_ROTOR_MAX_SIZE=5


    def createRandomModelName(self,length=100,cipherRotorCount=None):
        charSeq=""
        for i in range(length):
            randomChar=self.random.sample(CharIndexMap.charRange,1)[0]
            while(randomChar=="|"):
                randomChar=self.random.sample(CharIndexMap.charRange,1)[0]
            charSeq+=randomChar
        if cipherRotorCount:
            charSeq+="|"+str(cipherRotorCount)

        return Util.seqToStr(charSeq)


    def createMachineConfig(self,modelNo):
        model=modelNo
        cipherRotorCount=None
        if "|" in modelNo:
            tokens=modelNo.split("|")
            model=tokens[0]
            cipherRotorCount=int(tokens[1])
        seedStr=hashlib.sha512(model.encode("utf_8")).hexdigest()
        self.random=RandomGenerator(seedStr)
        machineCfg={}
        machineCfg["CIPHER_MODULE"]=self.createCipherModuleConfig(cipherRotorCount)
        machineCfg["SWAPPING_MODULE"]=self.createSwappingModuleConfig()
        return machineCfg

    def createCipherModuleConfig(self,cipherRotorCount=None):
        moduleCfg={}
        moduleCfg["ROTOR_STOCK"]=self.createCipherRotorStockConfig(cipherRotorCount)
        moduleCfg["REFLECTOR"]=self.createReflectorCfg()

        return moduleCfg

    def createSwappingModuleConfig(self):
        moduleCfg={}
        moduleCfg["SWAP_ROTOR_STOCK"]=self.createSwappingRotorStockConfig()
        return moduleCfg

    def createRotorStockConfig(self,rotorCount,rotorSize):
        rotorStock={}
        for i in range(rotorCount):
            rotorConfig=self.createRotorConfig(str(i),rotorSize)
            rotorStock[str(i)]=rotorConfig
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

    def createSwappingRotorStockConfig(self,rotorCount=None):
        if not rotorCount:
            rotorCount=self.random.nextInt(self.SWAP_ROTOR_COUNT_MIN,self.SWAP_ROTOR_COUNT_MAX)

        rotorsize=self.random.nextInt(self.SWAP_ROTOR_MIN_SIZE,self.SWAP_ROTOR_MAX_SIZE)

        return self.createRotorStockConfig(rotorCount,rotorsize)


    def getShuffledSequence(self,seq=None):
        if not seq:
            seq=CharIndexMap.getRange()
        shuffler=Shuffler(self.random)
        shSeq= shuffler.shuffleSeq(seq,self.random.nextInt())
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
        seq=self.shuffler.shuffleSeq(sequence,self.random.nextInt())
        while len(seq)>0:
            selectedPair=self.random.sample(seq,2)
            wiringTuples.append((selectedPair[0],selectedPair[1]))
            wiringTuples.append((selectedPair[1],selectedPair[0]))
            seq.remove(selectedPair[0])
            seq.remove(selectedPair[1])
        result=Util.convertTupleListToMap(wiringTuples)

        return result


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

