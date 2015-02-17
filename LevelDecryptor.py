from CharIndexMap import CharIndexMap
from ModernEnigma import ModernEnigma
from Level import Level
from Shuffler import Shuffler
from LevelEncryptor import LevelEncryptor
from Util import Util
from EnigmaStateManager import EnigmaStateManager
from LevelAnalyzer import LevelAnalyzer

class LevelDecryptor(LevelEncryptor):
    def __init__(self,baseMachine,levelMachine,level,stateManager=None,streamConverter=None):
        self.baseMachine=baseMachine
        self.levelMachine=levelMachine
        self.level=level
        self.streamConverter=streamConverter
        self.shuffler=Shuffler()
        self.stateManager=stateManager
        if not stateManager:
            self.stateManager=EnigmaStateManager()
        self.levelAnalyzer=LevelAnalyzer(baseMachine,levelMachine,level,self.stateManager)
        self.M1p_ph0=None
        self.M1p_ph1=None
        self.resetMachniesSettings()

    def decryptPhase(self,id,Ms1,Mp1,Ms2,machine1,machine2,m1BlkSize,m2BlkSize,seq):
        x=self.decryptSequence(seq,Ms2,m2BlkSize[id],self.level.l[id],self.level.xor[id])
        SEMsg=self.decryptSequence(x,Ms1,m1BlkSize[id],self.level.k[id],self.level.xor[id])
        EMsg=self.shuffler.deshuffleSeq(SEMsg,self.level.s[id])
        paddedM1pLength=len(Util.padSequence(range(machine1.getCipherRotorsCount()),m2BlkSize[id]))
        EM1p=EMsg[0:paddedM1pLength]
        Msg_M1p=EMsg[paddedM1pLength::]
        M1p=self.decryptSequence(EM1p,Ms2,m2BlkSize[id],self.level.i[id],self.level.xor[id])

        """adjust machine MpMc for ID of Mp1 """
        clonedMpMc=machine2.clone()
        clonedMpMc.adjustWindowDisplay(M1p)
        M1PNeededStates=self.levelAnalyzer.calculateNeededStatesForSeqLen(len(Msg_M1p),m2BlkSize[id])
        self.stateManager.generateMachineState(Mp1,clonedMpMc,M1PNeededStates)

        Msg=self.decryptSequence(Msg_M1p,Mp1,m1BlkSize[id],self.level.j[id],self.level.xor[id])
        print("DECRYPT")
        print("ID:"+id)
        print("y:")
        print(seq)
        print("x:")
        print(x)
        print("SEMsg:")
        print(SEMsg)
        print("EMsg:")
        print(EMsg)
        print("EM1p:")
        print(EM1p)
        print("Msg_M1p:")
        print(Msg_M1p)
        print("M1p:")
        print(M1p)
        print("Msg:")
        print(Msg)

        return Msg


    def decryptSequence(self,seq,machineId,blkSize,times=1,xorSeedValue=0):
        result=seq
        for t in range(times):
            result=self.processSeq(result,machineId,blkSize)

        result=self.applyXor(result,xorSeedValue)
        result=self.performUnPadding(result,blkSize)

        return result

    def decryptLevel(self,verbose=False):
        E=self.level.outputMsg
        if self.streamConverter:
            E=self.streamConverter.convertInput(E)
        self.generateNeededBaseStatesForLevel(len(E))
        phaseDecOut=self.decryptPhase("1","Ms","Mp","Bs",self.baseMachine,self.levelMachine,self.level.levelMcBlkSize,self.level.baseMcBlkSize,E)
        phaseDecOut=self.decryptPhase("0","Bs","Bp","Ms",self.levelMachine,self.baseMachine,self.level.baseMcBlkSize,self.level.levelMcBlkSize,phaseDecOut)
        self.stateManager.finished=True
        self.level.inputMsg=phaseDecOut
        if self.streamConverter:
            self.level.inputMsg=self.streamConverter.convertInput(msg)
        return self.level

    def generateNeededBaseStatesForLevel(self,seqLen):
        neededStatesMap=self.levelAnalyzer.analyzeNeededStatesForDecryptLevel()
        self.stateManager.generateMachineState("Bs",self.baseMachine.clone(),neededStatesMap["Bs"])
        self.stateManager.generateMachineState("Ms",self.levelMachine.clone(),neededStatesMap["Ms"])
    def performUnPadding(self,seq,blkSize=1):
        return Util.unpadSequence(seq)



