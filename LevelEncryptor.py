from RandomGenerator import RandomGenerator
from CharIndexMap import CharIndexMap
from ModernEnigma import ModernEnigma
from Level import Level
from Shuffler import Shuffler
from Util import Util
from EnigmaStateManager import EnigmaStateManager

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

        self.resetMachniesSettings()

    def resetMachniesSettings(self):
        self.baseMachine.adjustMachineSettings(self.level.baseStg)
        self.levelMachine.adjustMachineSettings(self.level.levelStg)


    def encryptPhase(self,id,machine1,machine2,m1BlkSize,m2BlkSize,seq):
        M1p=self.generatePerMsgWindowSetting(machine1)
        EM1p=self.encryptSequence(M1p,machine2,m2BlkSize[id],self.level.i[id],self.level.xor[id])
        Msg_M1p=self.encryptSequence(seq,machine1,m1BlkSize[id],self.level.j[id],self.level.xor[id],M1p)
        EMsg=EM1p+Msg_M1p
        SEMsg=Shuffler.shuffleSeq(EMsg,self.level.s[id])
        x=self.encryptSequence(SEMsg,machine1,m1BlkSize[id],self.level.k[id],self.level.xor[id])
        y=self.encryptSequence(x,machine2,m2BlkSize[id],self.level.l[id],self.level.xor[id])
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

        phaseEncOut=self.encryptPhase("0",self.baseMachine,self.levelMachine,self.level.baseMcBlkSize,self.level.levelMcBlkSize,seq)
        phaseEncOut=self.encryptPhase("1",self.levelMachine,self.baseMachine,self.level.levelMcBlkSize,self.level.baseMcBlkSize,phaseEncOut)
        self.level.outputMsg=phaseEncOut
        if self.streamConverter:
            self.level.outputMsg=self.streamConverter.convertOutput(E)
        return self.level
    def calculateNeededStatesForSeqLen(self,seqLen,blkSize):
        paddedSeqLen=Util.calculatePaddingForSeqLen(seqLen,blkSize)
        result= paddedSeqLen//blkSize
        return result
    def  calculateNeededStatesForPhase(self,id,m1,m2,m1BlkSize,m2BlkSize,seqLen):
        result={}
        M1PLen=m1.getCipherRotorsCount()
        EM1pLen=Util.calculatePaddingForSeqLen(M1PLen,m2BlkSize[id])
        EM1PNeededStates=self.calculateNeededStatesForSeqLen(M1PLen,m2BlkSize[id])

        Msg_M1pLen=Util.calculatePaddingForSeqLen(seqLen,m1BlkSize[id])
        Msg_M1pNeededStates=self.calculateNeededStatesForSeqLen(seqLen,m1BlkSize[id])

        SEMsgLen=EM1pLen+Msg_M1pLen
        xLen=Util.calculatePaddingForSeqLen(SEMsgLen,m1BlkSize[id])
        xNeededStates=self.calculateNeededStatesForSeqLen(SEMsgLen,m1BlkSize[id])

        yLen=Util.calculatePaddingForSeqLen(xLen,m2BlkSize[id])
        yNeedStates=self.calculateNeededStatesForSeqLen(xLen,m2BlkSize[id])

        result["EM1PNeededStates"]=EM1PNeededStates
        result["Msg_M1pNeededStates"]=Msg_M1pNeededStates
        result["xNeededStates"]=xNeededStates
        result["yNeedStates"]=yNeedStates
        result["yLen"]=yLen
        return result

    def generateNeededStatesForLevel(self,seqLen):
        phase0=self.calculateNeededStatesForPhase("0",self.baseMachine,self.levelMachine,self.level.baseMcBlkSize,self.level.levelMcBlkSize,seqLen)
        phase1=self.calculateNeededStatesForPhase("1",self.levelMachine,self.baseMachine,self.level.levelMcBlkSize,self.level.baseMcBlkSize,phase0["yLen"])

        BsStates=max(phase0["xNeededStates"],phase1["EM1PNeededStates"],phase1["yNeedStates"])
        BpStates=phase0["Msg_M1pNeededStates"]
        MsStates=max(phase0["EM1PNeededStates"],phase0["yNeedStates"],phase1["EM1PNeededStates"],phase1["xNeededStates"])
        MpStates=phase1["Msg_M1pNeededStates"]

        self.stateManager.generateMachineState("Bs",self.baseMachine.clone(),BsStates)
        self.stateManager.generateMachineState("Ms",self.levelMachine.clone(),MsStates)

        M1p_ph0=self.generatePerMsgWindowSetting(self.baseMachine)
        BpMachine=self.baseMachine.clone()
        BpMachine.adjustWindowDisplay(M1p_ph0)
        self.stateManager.generateMachineState("Bp",BpMachine,BpStates)

        M1p_ph1=self.generatePerMsgWindowSetting(self.levelMachine)
        MpMachine=self.levelMachine.clone()
        MpMachine.adjustWindowDisplay(M1p_ph1)
        self.stateManager.generateMachineState("Mp",MpMachine,MpStates)



    def encryptSequence(self,seq,machine,blkSize,times=1,xorSeedValue=0,displayStg=None):
        result=seq
        result=self.performPadding(result,blkSize)

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
            result+=machine.processKeyListPress(chunk)
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
