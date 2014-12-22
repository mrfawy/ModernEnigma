from random import Random
from CharIndexMap import CharIndexMap
from ModernEnigma import ModernEnigma
from Level import Level
from Shuffler import Shuffler
from LevelEncryptor import LevelEncryptor

class LevelDecryptor(LevelEncryptor):
    def __init__(self,baseMachine,levelMachine,level,random=None,streamConverter=None):
        self.baseMachine=baseMachine
        self.levelMachine=levelMachine
        self.level=level
        self.streamConverter=streamConverter
        if random==None:
            self.random=Random()
        self.shuffler=Shuffler()

    def decryptLevel(self):

        # print("==========DECRYPT===========")
        E=self.level.outputMsg
        if self.streamConverter:
            E=self.streamConverter.convertInput(E)
        # print("E: ")
        # print(E)
        R=self.encryptSequence(E,self.baseMachine,self.level.n_secondBsEncTimes)
        # print("R: ")
        # print(R)
        S=self.encryptSequence(R,self.levelMachine,self.level.m_secondMsEncTimes)
        # print("S: ")
        # print(S)
        W=self.shuffler.deshuffleSeq(S,self.level.s2_shuffleSeed)
        # print("W: ")
        # print(W)
        EMp=W[0:len(self.levelMachine.rotorList)]
        # print("EMp: ")
        # print(EMp)
        M0=W[len(self.levelMachine.rotorList)::]
        # print("M0: ")
        # print(M0)
        Mp=self.encryptSequence(EMp,self.levelMachine,self.level.k_PerMsgMsEncTimes)
        # print("Mp: ")
        # print(Mp)
        y=self.encryptSequence(M0,self.levelMachine,self.level.l_MmpEncTimes,Mp)
        # print("y: ")
        # print(y)
        x=self.encryptSequence(y,self.levelMachine,self.level.j_firstMsEncTimes)
        # print("x: ")
        # print(x)
        SEmsg=self.encryptSequence(x,self.baseMachine,self.level.i_firstBsEncTimes)
        # print("SEmsg: ")
        # print(SEmsg)
        Emsg=self.shuffler.deshuffleSeq(SEmsg,self.level.s1_shuffleSeed)
        # print("Emsg: ")
        # print(Emsg)
        EBp=Emsg[0:len(self.baseMachine.rotorList)]
        # print("EBp: ")
        # print(EBp)
        restMsg=Emsg[len(self.baseMachine.rotorList):len(Emsg)]
        # print("restMsg: ")
        # print(restMsg)
        Bp=self.encryptSequence(EBp,self.baseMachine,self.level.p_BpEncTimes)
        # print("Bp: ")
        # print(Bp)
        msg=self.encryptSequence(restMsg,self.baseMachine,self.level.o_PerMsgBpEncTimes,Bp)
        # print("msg: ")
        # print(msg)
        self.level.inputMsg=msg
        if self.streamConverter:
            self.level.inputMsg=self.streamConverter.convertInput(msg)
        return self.level



