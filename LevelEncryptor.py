from RandomGenerator import RandomGenerator
from CharIndexMap import CharIndexMap
from ModernEnigma import ModernEnigma
from Level import Level
from Shuffler import Shuffler
from Util import Util
from EnigmaStateManager import EnigmaStateManager

class LevelEncryptor(object):
    def __init__(self,baseMachine,levelMachine,level,stateManager=None,seed=None,streamConverter=None):
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
        self.generateNeededMachineStates()
        seq=self.level.inputMsg
        if self.streamConverter:
            seq=self.streamConverter.convertInput(msg)

        phaseEncOut=self.encryptPhase("0",self.baseMachine,self.levelMachine,self.level.baseMcBlkSize,self.level.levelMcBlkSize,seq)
        phaseEncOut=self.encryptPhase("1",self.levelMachine,self.baseMachine,self.level.levelMcBlkSize,self.level.baseMcBlkSize,phaseEncOut)
        self.level.outputMsg=phaseEncOut
        if self.streamConverter:
            self.level.outputMsg=self.streamConverter.convertOutput(E)
        return self.level
    def calculateNeededStatesForSeq(self,seqLen,blkSize):
        paddedSeqLen=Util.calculatePaddingForSeqlength(seqLen,blkSize)
        result= paddedSeqLen//blkSize
        return result
    def  calculateNeededStatesForPhase(self,id,m1,m2,m1BlkSize,m2BlkSize,seqLen):
        result={}
        M1PLen=m1.getCipherRotorsCount()
        EM1pLen=Util.calculatePaddingForSeqlength(M1PLen,m2BlkSize[id])
        EM1PNeededStates=self.calculateNeededState(M1PLen,m2BlkSize[id])

        Msg_M1pLen=Util.calculatePaddingForSeqlength(seqLen,m1BlkSize[id])
        Msg_M1pNeededStates=self.calculateNeededStates(seqLen,m1BlkSize[id])

        SEMsgLen=EM1pLen+Msg_M1pLen
        xLen=Util.calculatePaddingForSeqlength(SEMsgLen,m1BlkSize[id])
        xNeededStates=self.calculateNeededStates(SEMsgLen,m1BlkSize[id])

        yLen=Util.calculatePaddingForSeqlength(xLen,m2BlkSize[id])
        yNeedStates=self.calculateNeededStates(xLen,m2BlkSize[id])

        result["EM1PNeededStates"]=EM1PNeededStates
        result["Msg_M1pNeededStates"]=Msg_M1pNeededStates
        result["xNeededStates"]=xNeededStates
        result["yNeedStates"]=yNeedStates
        result["yLen"]=yLen
        return result

    def generateNeededStatesForLevel(self):
        phase0=self.calculateNeededStatesForPhase("0",self.baseMachine,self.levelMachine,self.level.baseMcBlkSize,self.level.levelMcBlkSize,len(seq))
        phase1=self.calculateNeededStatesForPhase("1",self.levelMachine,self.baseMachine,self.level.levelMcBlkSize,self.level.baseMcBlkSize,phase0["yLen"])

        BsStates=max(phase0["xNeededStates"],phase1["EM1PNeededStates"],phase1["yNeedStates"])
        BpStates=phase0["Msg_M1pNeededStates"]
        MsStates=max(phase0["EM1PNeededStates"],phase0["yNeedStates"],phase1["EM1PNeededStates"],phase1["xNeededStates"])
        MpStates=phase1["Msg_M1pNeededStates"]

        # self.resetMachniesSettings()
        # self.stateManager.generateMachineState("Bp",BpStates)
        # self.stateManager.generateMachineState("Mp",self.levelMachine,4)








    def generateNeededMachineStates(self):
        bsMcRotorCount=self.baseMachine.getCipherRotorsCount()
        LvMcRotorCount=self.levelMachine.getCipherRotorsCount()
        seqLen=len(self.level.inputMsg)

        BsNeededStates=0
        MsNeededStates=0
        BpNeededStates=0
        MpNeededStates=0

        """phase 0"""
        phaseMap={}
        phase0={}
        M1PLen=bsMcRotorCount
        EM1pLen=Util.calculatePaddingForSeqlength(M1PLen,self.level.levelMcBlkSize[0])

        EM1PNeededStates=self.calculateNeededState(M1PLen,self.level.levelMcBlkSize[0])
        MsNeededStates+=m1pNeededStates

        Msg_M1pLen=Util.calculatePaddingForSeqlength(seqLen,self.level.baseMcBlkSize[0])

        Msg_M1pNeededStates=self.calculateNeededStates(seqLen,self.level.baseMcBlkSize[0])
        BpNeededStates=Msg_M1pStates

        SEMsgLen=EM1pLen+Msg_M1pLen
        xLen=Util.calculatePaddingForSeqlength(SEMsgLen,self.level.baseMcBlkSize[0])
        xNeededStates=self.calculateNeededStates(SEMsgLen,self.level.baseMcBlkSize[0])

        yLen=Util.calculatePaddingForSeqlength(xLen,self.level.levelMcBlkSize[0])
        yNeedStates=self.calculateNeededStates(xLen,self.level.levelMcBlkSize[0])


        SEMsgLen=Util.calculatePaddingForSeqlength(seqLen,baseMcBlkSize)+EM1pLen
        SEMsgNeededStates=self.calculateNeededStates(SEMsgLen,


        BsNeededStates=self




        phase0["M1P"]={mc.getCipherRotorsCount(),





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
