from RandomGenerator import RandomGenerator
from CharIndexMap import CharIndexMap
from ModernEnigma import ModernEnigma
from Level import Level
from Shuffler import Shuffler
from Util import Util

class LevelEncryptor(object):
    def __init__(self,baseMachine,levelMachine,level,random=None,streamConverter=None):
        self.baseMachine=baseMachine
        self.levelMachine=levelMachine
        self.level=level
        self.random=random
        if not random:
            self.random=RandomGenerator()
        self.streamConverter=streamConverter
        self.shuffler=Shuffler()
        self.initLevelValues()
    def initLevelValues(self):
        min=3
        max=16
        self.level.i[0]=self.random.nextInt(min,max)
        self.level.i[1]=self.random.nextInt(min,max)
        self.level.j[0]=self.random.nextInt(min,max)
        self.level.j[1]=self.random.nextInt(min,max)
        self.level.k[0]=self.random.nextInt(min,max)
        self.level.k[1]=self.random.nextInt(min,max)
        self.level.l[0]=self.random.nextInt(min,max)
        self.level.l[1]=self.random.nextInt(min,max)
        self.level.s[0]=self.random.nextInt(min,max)
        self.level.s[1]=self.random.nextInt(min,max)
        self.level.st[0]=self.random.nextInt(min,max)
        self.level.st[1]=self.random.nextInt(min,max)
        self.level.baseMcBlkSize[0]=self.random.nextInt(1,self.baseMachine.getCipherRotorsSize())
        self.level.baseMcBlkSize[1]=self.random.nextInt(1,self.baseMachine.getCipherRotorsSize())
        self.level.levelMcBlkSize[0]=self.random.nextInt(1,self.levelMachine.getCipherRotorsSize())
        self.level.levelMcBlkSize[1]=self.random.nextInt(1,self.levelMachine.getCipherRotorsSize())

    def encryptPhase(self,id,machine1,machine2,m1BlkSize,m2BlkSize,seq):
        M1p=self.generatePerMsgWindowSetting(machine1)
        EM1p=self.encryptSequence(M1p,machine2,m2BlkSize[id],self.level.i[id])
        Msg_M1p=self.encryptSequence(seq,machine1,m1BlkSize[id],self.level.j[id],M1p)
        EMsg=EM1p+Msg_M1p
        SEMsg=self.shuffler.shuffleSeq(EMsg,self.level.s[id])
        x=self.encryptSequence(SEMsg,machine1,m1BlkSize[id],self.level.k[id])
        y=self.encryptSequence(x,machine2,m2BlkSize[id],self.level.l[id])

        # print("ENCRYPT")
        # print("ID:"+str(id))
        # print("M1p:")
        # print(M1p)
        # print("EM1p:")
        # print(EM1p)
        # print("Msg_M1p:")
        # print(Msg_M1p)
        # print("Emsg:")
        # print(EMsg)
        # print("SEMsg:")
        # print(SEMsg)
        # print("x:")
        # print(x)
        # print("y:")
        # print(y)
        return y


    def encryptLevel(self,verbose=False):
        seq=self.level.inputMsg
        if self.streamConverter:
            seq=self.streamConverter.convertInput(msg)

        phaseEncOut=self.encryptPhase(0,self.baseMachine,self.levelMachine,self.level.baseMcBlkSize,self.level.levelMcBlkSize,seq)
        phaseEncOut=self.encryptPhase(1,self.levelMachine,self.baseMachine,self.level.levelMcBlkSize,self.level.baseMcBlkSize,phaseEncOut)
        self.level.outputMsg=phaseEncOut
        if self.streamConverter:
            self.level.outputMsg=self.streamConverter.convertOutput(E)
        return self.level


    def encryptSequence(self,seq,machine,blkSize,times=1,displayStg=None):
        result=[]
        if displayStg:
            machine.adjustWindowDisplay(displayStg)
        result=seq
        result=self.performAdjustPadding(result,blkSize)
        for t in range(times):
            result=self.processSeq(result,machine,blkSize)

        return result

    def processSeq(self,seq,machine,blkSize):
        result=[]
        preEncryptionStg=machine.getMachineSettings()
        startIndex=0
        endIndex=blkSize
        while endIndex<=len(seq):
            currentBlk=seq[startIndex:endIndex]
            currentBlk=self.performMappingBlockToRotor(currentBlk,machine.getCipherRotorsSize())
            result=result+machine.processKeyListPress(currentBlk)
            startIndex+=blkSize
            endIndex+=blkSize

        machine.adjustMachineSettings(preEncryptionStg)

        return result

    def performMappingBlockToRotor(self,blkSeq,rotorSize):
         return blkSeq

    def performAdjustPadding(self,seq,blkSize=1):
        return Util.padSequence(seq,blkSize)



    def generatePerMsgWindowSetting(self,mc):
        result=[]
        for i in range(mc.getCipherRotorsCount()):
            selectedOffset=self.random.sample(range(mc.getCipherRotorsSize()),1)[0]
            result.append(selectedOffset)
        return result
