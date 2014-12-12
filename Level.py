from ModernEnigma import ModernEnigma
import json

class Level(object):
    def __init__(self,baseMachineStg,levelMachineStg):
        self.baseStg=baseMachineStg
        self.levelStg=levelMachineStg
        self.inputMsg=""
        self.outputMsg=""
        self.i_firstBsEncTimes=0
        self.j_firstMsEncTimes=0
        self.k_PerMsgMsEncTimes=0
        self.l_MmpEncTimes=0
        self.m_secondMsEncTimes=0
        self.n_secondBsEncTimes=0
        self.s_shuffleSeed=0

    def toJson(self):
        jsonMap={}
        jsonMap["baseStg"]=self.baseStg
        jsonMap["levelStg"]=self.levelStg
        jsonMap["inputMsg"]=self.inputMsg
        jsonMap["outputMsg"]=self.outputMsg
        jsonMap["i_firstBsEncTimes"]=self.i_firstBsEncTimes
        jsonMap["j_firstMsEncTimes"]=self.j_firstMsEncTimes
        jsonMap["k_PerMsgMsEncTimes"]=self.k_PerMsgMsEncTimes
        jsonMap["l_MmpEncTimes"]=self.l_MmpEncTimes
        jsonMap["m_secondMsEncTimes"]=self.m_secondMsEncTimes
        jsonMap["n_secondBsEncTimes"]=self.n_secondBsEncTimes
        jsonMap["s_shuffleSeed"]=self.s_shuffleSeed
        return (json.dumps(jsonMap,sort_keys=True,indent=4, separators=(',', ': ')))
