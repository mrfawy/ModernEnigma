from Util import Util
class LevelAnalyzer(object):
    def __init__(self,baseMachine,levelMachine,level,stateManager=None):
        self.baseMachine=baseMachine
        self.levelMachine=levelMachine
        self.level=level
        self.stateManager=stateManager
        if not stateManager:
            self.stateManager=EnigmaStateManager()

    def analyzeNeededStatesForEncryptLevel(self):
        phase0=self.calculateNeededStatesForPhase("0",self.baseMachine,self.levelMachine,self.level.baseMcBlkSize,self.level.levelMcBlkSize,len(self.level.inputMsg))
        phase1=self.calculateNeededStatesForPhase("1",self.levelMachine,self.baseMachine,self.level.levelMcBlkSize,self.level.baseMcBlkSize,phase0["yLen"])

        BsStates=max(phase0["xNeededStates"],phase1["EM1PNeededStates"],phase1["yNeedStates"])
        BpStates=phase0["Msg_M1pNeededStates"]
        MsStates=max(phase0["EM1PNeededStates"],phase0["yNeedStates"],phase1["EM1PNeededStates"],phase1["xNeededStates"])
        MpStates=phase1["Msg_M1pNeededStates"]

        result={}
        result["Bs"]=BsStates
        result["Bp"]=BpStates
        result["Ms"]=MsStates
        result["Mp"]=MpStates

        return result
    def analyzeNeededStatesForDecryptLevel(self):
        seqLen=len(self.level.outputMsg)
        BsStatesPh1=self.calculateNeededStatesForSeqLen(seqLen,self.level.baseMcBlkSize["1"])
        BsStatesPh0=self.calculateNeededStatesForSeqLen(seqLen,self.level.baseMcBlkSize["0"])
        MsStatesPh1=self.calculateNeededStatesForSeqLen(seqLen,self.level.levelMcBlkSize["1"])
        MsStatesPh0=self.calculateNeededStatesForSeqLen(seqLen,self.level.levelMcBlkSize["0"])


        BsStates=max(BsStatesPh0,BsStatesPh1)
        MsStates=max(MsStatesPh0,MsStatesPh1)

        result={}
        result["Bs"]=BsStates
        result["Ms"]=MsStates

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

    def calculateNeededStatesForSeqLen(self,seqLen,blkSize):
        paddedSeqLen=Util.calculatePaddingForSeqLen(seqLen,blkSize)
        result= paddedSeqLen//blkSize
        return result
