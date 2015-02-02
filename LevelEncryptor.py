from RandomGenerator import RandomGenerator
from CharIndexMap import CharIndexMap
from ModernEnigma import ModernEnigma
from Level import Level
from Shuffler import Shuffler
from Util import Util
from EnigmaStateManager import EnigmaStateManager
from LevelAnalyzer import LevelAnalyzer

class LevelEncryptor(object):
    def __init__(self,baseMachine,levelMachine,level,seed=None,stateManager=None,streamConverter=None):
        self.baseMachine=baseMachine
        self.levelMachine=levelMachine
        self.level=level
        self.seed=seed
        self.random=RandomGenerator(seed)
        self.streamConverter=streamConverter
        self.resetMachniesSettings()
        self.stateManager=stateManager
        if not stateManager:
            self.stateManager=EnigmaStateManager()

        self.levelAnalayzer=LevelAnalyzer(baseMachine,levelMachine,level,seed,self.stateManager)
        self.M1p_ph0=None
        self.M1p_ph1=None

        self.resetMachniesSettings()

    def resetMachniesSettings(self):
        self.baseMachine.adjustMachineSettings(self.level.baseStg)
        self.levelMachine.adjustMachineSettings(self.level.levelStg)


    def encryptPhase(self,id,Ms1,Mp1,Ms2,Mp2,m1BlkSize,m2BlkSize,M1PerMsgStg,seq):
        EM1p=self.encryptSequence(M1PerMsgStg,Ms2,m2BlkSize[id],self.level.i[id],self.level.xor[id])
        Msg_M1p=self.encryptSequence(seq,Mp1,m1BlkSize[id],self.level.j[id],self.level.xor[id])
        EMsg=EM1p+Msg_M1p
        SEMsg=Shuffler.shuffleSeq(EMsg,self.level.s[id])
        x=self.encryptSequence(SEMsg,Ms1,m1BlkSize[id],self.level.k[id],self.level.xor[id])
        y=self.encryptSequence(x,Ms2,m2BlkSize[id],self.level.l[id],self.level.xor[id])
        #
        # print("ENCRYPT")
        # print("ID:"+id)
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

        self.generateNeededStatesForLevel(len(seq))

        phaseEncOut=self.encryptPhase("0","Bs","Bp","Ms","Mp",self.level.baseMcBlkSize,self.level.levelMcBlkSize,self.M1p_ph0,seq)
        phaseEncOut=self.encryptPhase("1","Ms","Mp","Bs","Bp",self.level.levelMcBlkSize,self.level.baseMcBlkSize,self.M1p_ph1,phaseEncOut)
        self.level.outputMsg=phaseEncOut
        if self.streamConverter:
            self.level.outputMsg=self.streamConverter.convertOutput(E)
        return self.level

    def generateNeededStatesForLevel(self,seqLen):
        neededStatesMap=self.levelAnalayzer.analyzeNeededStatesForLevel()
        self.stateManager.generateMachineState("Bs",self.baseMachine.clone(),neededStatesMap["Bs"])
        self.stateManager.generateMachineState("Ms",self.levelMachine.clone(),neededStatesMap["Ms"])

        self.M1p_ph0=self.generatePerMsgWindowSetting(self.baseMachine)
        BpMachine=self.baseMachine.clone()
        BpMachine.adjustWindowDisplay(self.M1p_ph0)
        self.stateManager.generateMachineState("Bp",BpMachine,neededStatesMap["Bs"])

        self.M1p_ph1=self.generatePerMsgWindowSetting(self.levelMachine)
        MpMachine=self.levelMachine.clone()
        MpMachine.adjustWindowDisplay(self.M1p_ph1)
        self.stateManager.generateMachineState("Mp",MpMachine,neededStatesMap["Mp"])

    def encryptSequence(self,seq,machineId,blkSize,times=1,xorSeedValue=0):
        result=seq
        result=self.performPadding(result,blkSize)

        result=self.applyXor(result,xorSeedValue)
        for t in range(times):
            result=self.processSeq(result,machineId,blkSize)

        return result

    def processSeq(self,seq,machineId,blkSize):
        result=[]
        seqChunks=Util.divideIntoChunks(seq,blkSize)
        index=0
        for chunk in seqChunks:
            state=self.stateManager.retreiveMachineState(machineId,index)
            result+=self.processChunkSeqByState(state,chunk)
            index+=1
        return result
    def processChunkSeqByState(self,state,seq):
        result=[]
        for s in seq:
            result.append(state[s])
        return result

    def performPadding(self,seq,blkSize=1):
        return Util.padSequence(seq,blkSize,self.seed)

    def applyXor(self,seq,xorSeedValue):
        hashedSeed=Util.hashString(str(xorSeedValue))
        randomXor=RandomGenerator(hashedSeed)
        result=[]
        for s in seq:
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
