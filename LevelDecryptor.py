from random import Random
from CharIndexMap import CharIndexMap
from ModernEnigma import ModernEnigma
from Level import Level
from Shuffler import Shuffler

class LevelDecryptor(object):
    def __init__(self,baseMachine,levelMachine,level,random=None):
        self.baseMachine=baseMachine
        self.levelMachine=levelMachine
        self.level=level
        if random==None:
            self.random=Random()
            self.random.seed(123)
        self.shuffler=Shuffler()

    def decryptLevel(self):
        print("==========DECRYPT===========")
        E=self.level.outputMsg
        print("E: "+E)
        R=self.encryptText(E,self.baseMachine,self.level.n_secondBsEncTimes)
        print("R: "+R)
        S=self.encryptText(R,self.levelMachine,self.level.m_secondMsEncTimes)
        print("S: "+S)
        W=self.shuffler.deshuffle(S,self.level.s_shuffleSeed)
        print("W: "+W)
        EMp=W[0:len(self.levelMachine.rotorList)]
        print("EMp: "+EMp)
        M0=W[len(self.levelMachine.rotorList)::]
        print("M0: "+M0)
        Mp=self.encryptText(EMp,self.levelMachine,self.level.k_PerMsgMsEncTimes)
        print("Mp: "+Mp)
        y=self.encryptText(M0,self.levelMachine,self.level.l_MmpEncTimes,Mp)
        print("y: "+y)
        x=self.encryptText(y,self.levelMachine,self.level.j_firstMsEncTimes)
        print("x: "+x)
        Emsg=self.encryptText(x,self.baseMachine,self.level.i_firstBsEncTimes)
        print("Emsg: "+Emsg)
        EBp=Emsg[0:len(self.baseMachine.rotorList)]
        print("EBp: "+EBp)
        restMsg=Emsg[len(self.baseMachine.rotorList):len(Emsg)]
        print("restMsg: "+restMsg)
        Bp=self.encryptText(EBp,self.baseMachine,1)
        print("Bp: "+Bp)
        msg=self.encryptText(restMsg,self.baseMachine,1,Bp)
        print("msg: "+msg)
        self.level.inputMsg=msg
        return self.level





    def encryptText(self,text,machine,times=1,displayStg=None):
        result=""
        preEncryptionStg=machine.getMachineSettings()
        if displayStg:
            machine.adjustWindowDisplay(displayStg)

        for c in text:
            result+=machine.processKeyPress(c)
        machine.adjustMachineSettings(preEncryptionStg)
        return result




    def generatePerMsgWindowSetting(self,machine):
        randomRange= sorted(CharIndexMap.getRange(), key=lambda k: self.random.random())
        result=""
        for i in range(len(machine.rotorList)):
            result+=randomRange[i]
        return result
