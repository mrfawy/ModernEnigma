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

    def decryptLevel(self,verbose=False):

        if verbose:
            print("==========DECRYPT===========")
        E=self.level.outputMsg
        if self.streamConverter:
            E=self.streamConverter.convertInput(E)
        if verbose:
            print("E: ")
            print(E)
        R=self.encryptSequence(E,self.baseMachine,self.level.n_secondBsEncTimes)
        if verbose:
            print("R: ")
            print(R)
        S=self.encryptSequence(R,self.levelMachine,self.level.m_secondMsEncTimes)
        if verbose:
            print("S: ")
            print(S)
        W=self.shuffler.deshuffleSeq(S,self.level.s2_shuffleSeed)
        if verbose:
            print("W: ")
            print(W)
        EMp=W[0:len(self.levelMachine.rotorList)]
        if verbose:
            print("EMp: ")
            print(EMp)
        M0=W[len(self.levelMachine.rotorList)::]
        if verbose:
            print("M0: ")
            print(M0)
        Mp=self.encryptSequence(EMp,self.levelMachine,self.level.k_PerMsgMsEncTimes)
        if verbose:
            print("Mp: ")
            print(Mp)
        y=self.encryptSequence(M0,self.levelMachine,self.level.l_MmpEncTimes,Mp)
        if verbose:
            print("y: ")
            print(y)
        x=self.encryptSequence(y,self.levelMachine,self.level.j_firstMsEncTimes)
        if verbose:
            print("x: ")
            print(x)
        SEmsg=self.encryptSequence(x,self.baseMachine,self.level.i_firstBsEncTimes)
        if verbose:
            print("SEmsg: ")
            print(SEmsg)
        Emsg=self.shuffler.deshuffleSeq(SEmsg,self.level.s1_shuffleSeed)
        if verbose:
            print("Emsg: ")
            print(Emsg)
        EBp=Emsg[0:len(self.baseMachine.rotorList)]
        if verbose:
            print("EBp: ")
            print(EBp)
        restMsg=Emsg[len(self.baseMachine.rotorList):len(Emsg)]
        if verbose:
            print("restMsg: ")
            print(restMsg)
        Bp=self.encryptSequence(EBp,self.baseMachine,self.level.p_BpEncTimes)
        if verbose:
            print("Bp: ")
            print(Bp)
        msg=self.encryptSequence(restMsg,self.baseMachine,self.level.o_PerMsgBpEncTimes,Bp)
        if verbose:
            print("msg: ")
            print(msg)
        self.level.inputMsg=msg
        if self.streamConverter:
            self.level.inputMsg=self.streamConverter.convertInput(msg)
        return self.level



