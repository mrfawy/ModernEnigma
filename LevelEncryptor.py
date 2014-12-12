from random import Random
from CharIndexMap import CharIndexMap
from ModernEnigma import ModernEnigma
from Level import Level
from Shuffler import Shuffler

class LevelEncryptor(object):
    def __init__(self,baseMachine,levelMachine,level,random=None):
        self.baseMachine=baseMachine
        self.levelMachine=levelMachine
        self.level=level
        if random==None:
            self.random=Random()
        self.shuffler=Shuffler()
        self.initLevelValues()
    def initLevelValues(self):
        min=1
        max=9
        self.level.i_firstBsEncTimes=self.random.randint(min,max)
        self.level.j_firstMsEncTimes=self.random.randint(min,max)
        self.level.k_PerMsgMsEncTimes=self.random.randint(min,max)
        self.level.l_MmpEncTimes=self.random.randint(min,max)
        self.level.m_secondMsEncTimes=self.random.randint(min,max)
        self.level.n_secondBsEncTimes=self.random.randint(min,max)
        self.level.s_shuffleSeed=self.random.randint(min,max)



    def encryptLevel(self):
        msg=self.level.inputMsg
        Bp=self.generatePerMsgWindowSetting(self.baseMachine)
        EBp=self.encryptText(Bp,self.baseMachine,1)
        Emsg=EBp+self.encryptText(msg,self.baseMachine,1,Bp)
        x=self.encryptText(Emsg,self.baseMachine,self.level.i_firstBsEncTimes)
        y=self.encryptText(x,self.baseMachine,self.level.j_firstMsEncTimes)
        Mp=self.generatePerMsgWindowSetting(self.levelMachine)
        EMp=self.encryptText(Mp,self.levelMachine,self.level.k_PerMsgMsEncTimes)
        M0=self.encryptText(y,self.levelMachine,self.level.l_MmpEncTimes,Mp)
        W=EMp+M0
        S=self.shuffler.shuffle(W,self.level.s_shuffleSeed)
        R=self.encryptText(S,self.levelMachine,self.level.m_secondMsEncTimes)
        E=self.encryptText(R,self.baseMachine,self.level.n_secondBsEncTimes)

        self.level.outputMsg=E
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
