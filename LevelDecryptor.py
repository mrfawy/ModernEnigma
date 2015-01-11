from CharIndexMap import CharIndexMap
from ModernEnigma import ModernEnigma
from Level import Level
from Shuffler import Shuffler
from LevelEncryptor import LevelEncryptor
from Util import Util

class LevelDecryptor(LevelEncryptor):
    def __init__(self,baseMachine,levelMachine,level,streamConverter=None):
        self.baseMachine=baseMachine
        self.levelMachine=levelMachine
        self.level=level
        self.streamConverter=streamConverter
        self.shuffler=Shuffler()
        self.resetMachniesSettings()

    def decryptPhase(self,id,machine1,machine2,m1BlkSize,m2BlkSize,seq):
        x=self.decryptSequence(seq,machine2,m2BlkSize[id],self.level.l[id],self.level.xor[id])
        SEMsg=self.decryptSequence(x,machine1,m1BlkSize[id],self.level.k[id],self.level.xor[id])
        EMsg=self.shuffler.deshuffleSeq(SEMsg,self.level.s[id])
        paddedM1pLength=len(Util.padSequence(range(machine1.getCipherRotorsCount()),m2BlkSize[id]))
        EM1p=EMsg[0:paddedM1pLength]
        Msg_M1p=EMsg[paddedM1pLength::]
        M1p=self.decryptSequence(EM1p,machine2,m2BlkSize[id],self.level.i[id],self.level.xor[id])
        Msg=self.decryptSequence(Msg_M1p,machine1,m1BlkSize[id],self.level.j[id],self.level.xor[id],M1p)
        # print("DECRYPT")
        # print("ID:"+str(id))
        # print("y:")
        # print(seq)
        # print("x:")
        # print(x)
        # print("SEMsg:")
        # print(SEMsg)
        # print("EMsg:")
        # print(EMsg)
        # print("EM1p:")
        # print(EM1p)
        # print("Msg_M1p:")
        # print(Msg_M1p)
        # print("M1p:")
        # print(M1p)
        # print("Msg:")
        # print(Msg)

        return Msg


    def decryptSequence(self,seq,machine,blkSize,times=1,xorValue=0,displayStg=None):
        result=[]
        if displayStg:
            machine.adjustWindowDisplay(displayStg)
        result=seq
        for t in range(times):
            result=self.processSeq(result,machine,blkSize)

        result=self.applyXor(result,xorValue)
        result=self.performAdjustPadding(result,blkSize)

        return result

    def decryptLevel(self,verbose=False):
        E=self.level.outputMsg
        if self.streamConverter:
            E=self.streamConverter.convertInput(E)
        self.resetMachniesSettings()
        phaseDecOut=self.decryptPhase(1,self.levelMachine,self.baseMachine,self.level.levelMcBlkSize,self.level.baseMcBlkSize,E)
        self.resetMachniesSettings()
        phaseDecOut=self.decryptPhase(0,self.baseMachine,self.levelMachine,self.level.baseMcBlkSize,self.level.levelMcBlkSize,phaseDecOut)
        self.level.inputMsg=phaseDecOut
        if self.streamConverter:
            self.level.inputMsg=self.streamConverter.convertInput(msg)
        return self.level

    def performAdjustPadding(self,seq,blkSize=1):
        if(len(seq)==0):
            return seq
        return Util.unpadSequence(seq)



