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
            self.random.seed(123)
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
        print("MSG: "+msg)
        Bp=self.generatePerMsgWindowSetting(self.baseMachine)
        print("Bp: "+Bp)
        EBp=self.encryptText(Bp,self.baseMachine,1)
        print("EBp: "+EBp)
        Emsg=EBp+self.encryptText(msg,self.baseMachine,1,Bp)
        print("Emsg: "+Emsg)
        x=self.encryptText(Emsg,self.baseMachine,self.level.i_firstBsEncTimes)
        print("x: "+x)
        y=self.encryptText(x,self.levelMachine,self.level.j_firstMsEncTimes)
        print("y: "+y)
        Mp=self.generatePerMsgWindowSetting(self.levelMachine)
        print("Mp: "+Mp)
        EMp=self.encryptText(Mp,self.levelMachine,self.level.k_PerMsgMsEncTimes)
        print("EMp: "+EMp)
        M0=self.encryptText(y,self.levelMachine,self.level.l_MmpEncTimes,Mp)
        print("M0: "+M0)
        W=EMp+M0
        print("W: "+W)
        S=self.shuffler.shuffle(W,self.level.s_shuffleSeed)
        print("S: "+S)
        R=self.encryptText(S,self.levelMachine,self.level.m_secondMsEncTimes)
        print("R: "+R)
        E=self.encryptText(R,self.baseMachine,self.level.n_secondBsEncTimes)
        print("E: "+E)

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
