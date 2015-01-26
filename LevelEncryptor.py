from RandomGenerator import RandomGenerator
from CharIndexMap import CharIndexMap
from ModernEnigma import ModernEnigma
from Level import Level
from Shuffler import Shuffler
from Util import Util

class LevelEncryptor(object):
    def __init__(self,baseMachine,levelMachine,level,seed=None,streamConverter=None):
        self.baseMachine=baseMachine
        self.levelMachine=levelMachine
        self.level=level
        self.random=RandomGenerator(seed)
        self.streamConverter=streamConverter
        self.shuffler=Shuffler()
        self.resetMachniesSettings()

    def resetMachniesSettings(self):
        self.baseMachine.adjustMachineSettings(self.level.baseStg)
        self.levelMachine.adjustMachineSettings(self.level.levelStg)


    def encryptPhase(self,id,machine1,machine2,m1BlkSize,m2BlkSize,seq):
        M1p=self.generatePerMsgWindowSetting(machine1)
        EM1p=self.encryptSequence(M1p,machine2,m2BlkSize[id],self.level.i[id],self.level.xor[id])
        Msg_M1p=self.encryptSequence(seq,machine1,m1BlkSize[id],self.level.j[id],self.level.xor[id],M1p)
        EMsg=EM1p+Msg_M1p
        SEMsg=self.shuffler.shuffleSeq(EMsg,self.level.s[id])
        x=self.encryptSequence(SEMsg,machine1,m1BlkSize[id],self.level.k[id],self.level.xor[id])
        y=self.encryptSequence(x,machine2,m2BlkSize[id],self.level.l[id],self.level.xor[id])
        #
        # print("ENCRYPT")
        # print("ID:"+str(id))
        # print("Msg:")
        # print(seq)
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

        self.resetMachniesSettings()
        phaseEncOut=self.encryptPhase("0",self.baseMachine,self.levelMachine,self.level.baseMcBlkSize,self.level.levelMcBlkSize,seq)
        self.resetMachniesSettings()
        phaseEncOut=self.encryptPhase("1",self.levelMachine,self.baseMachine,self.level.levelMcBlkSize,self.level.baseMcBlkSize,phaseEncOut)
        self.level.outputMsg=phaseEncOut
        # if self.streamConverter:
            # self.level.outputMsg=self.streamConverter.convertOutput(E)
        return self.level


    def encryptSequence(self,seq,machine,blkSize,times=1,xorSeedValue=0,displayStg=None):
        result=[]
        result=seq
        result=self.performAdjustPadding(result,blkSize)
        if(len(result)%blkSize !=0):
            print("encrpyt seq , invalid padding ")

        result=self.applyXor(result,xorSeedValue)
        for t in range(times):
            self.resetMachniesSettings()
            if displayStg:
                machine.adjustWindowDisplay(displayStg)
            result=self.processSeq(result,machine,blkSize)

        return result

    def processSeq(self,seq,machine,blkSize):
        result=[]
        seqChunks=Util.divideIntoChunks(seq,blkSize)
        for chunk in seqChunks:
            result.append(machine.processKeyListPress(chunk))
        return result

    def performAdjustPadding(self,seq,blkSize=1):
        return Util.padSequence(seq,blkSize,self.random.nextInt())

    def applyXor(self,seq,xorSeedValue):
        randomXor=RandomGenerator(xorSeedValue)
        result=[]
        for s in seq:
            xorValue=randomXor.nextInt()
            xorResult=s^xorValue
            rangeSize=CharIndexMap.getRangeSize()
            while(xorResult>rangeSize):
                xorValue=randomXor.nextInt()
                xorResult=s^xorValue
            result.append(xorResult)
        return result




    def generatePerMsgWindowSetting(self,mc):
        result=[]
        for i in range(mc.getCipherRotorsCount()):
            rotorOffsetRange=range(mc.getCipherRotorsSize())
            selectedOffset=self.random.sample(rotorOffsetRange,1)[0]
            result.append(selectedOffset)
        return result
