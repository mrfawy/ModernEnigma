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
        self.o_PerMsgBpEncTimes=0
        self.p_BpEncTimes=0
        self.s1t_shuffle1Times=0
        self.s2t_shuffle2Times=0
        self.s1_shuffleSeed=0
        self.s2_shuffleSeed=0

    def toJson(self):
        jsonMap={}
        jsonMap["baseStg"]=self.baseStg.getAsMap()
        jsonMap["levelStg"]=self.levelStg.getAsMap()
        jsonMap["inputMsg"]=self.inputMsg
        jsonMap["outputMsg"]=self.outputMsg
        jsonMap["i_firstBsEncTimes"]=self.i_firstBsEncTimes
        jsonMap["j_firstMsEncTimes"]=self.j_firstMsEncTimes
        jsonMap["k_PerMsgMsEncTimes"]=self.k_PerMsgMsEncTimes
        jsonMap["l_MmpEncTimes"]=self.l_MmpEncTimes
        jsonMap["m_secondMsEncTimes"]=self.m_secondMsEncTimes
        jsonMap["n_secondBsEncTimes"]=self.n_secondBsEncTimes

        jsonMap["o_PerMsgBpEncTimes"]=self.o_PerMsgBpEncTimes
        jsonMap["p_BpEncTimes"]=self.p_BpEncTimes
        jsonMap["s1t_shuffle1Times"]=self.s1t_shuffle1Times
        jsonMap["s2t_shuffle2Times"]=self.s2t_shuffle2Times
        jsonMap["s1_shuffleSeed"]=self.s1_shuffleSeed
        jsonMap["s2_shuffleSeed"]=self.s2_shuffleSeed
        return (json.dumps(jsonMap,sort_keys=True,indent=4, separators=(',', ': ')))
