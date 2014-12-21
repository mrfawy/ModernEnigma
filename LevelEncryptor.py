from RandomGenerator import RandomGenerator
from CharIndexMap import CharIndexMap
from ModernEnigma import ModernEnigma
from Level import Level
from Shuffler import Shuffler

class LevelEncryptor(object):
    def __init__(self,baseMachine,levelMachine,level,random=None,streamConverter=None):
        self.baseMachine=baseMachine
        self.levelMachine=levelMachine
        self.level=level
        self.random=random
        if not random:
            self.random=RandomGenerator()
        self.streamConverter=streamConverter
        self.shuffler=Shuffler()
        self.initLevelValues()
    def initLevelValues(self):
        min=1
        max=9
        self.level.i_firstBsEncTimes=self.random.nextInt(min,max)
        self.level.j_firstMsEncTimes=self.random.nextInt(min,max)
        self.level.k_PerMsgMsEncTimes=self.random.nextInt(min,max)
        self.level.l_MmpEncTimes=self.random.nextInt(min,max)
        self.level.m_secondMsEncTimes=self.random.nextInt(min,max)
        self.level.n_secondBsEncTimes=self.random.nextInt(min,max)
        self.level.o_PerMsgBpEncTimes=self.random.nextInt(min,max)
        self.level.p_BpEncTimes=self.random.nextInt(min,max)
        self.level.s1_shuffleSeed=self.random.nextInt(min,max)
        self.level.s1t_shuffle1Times=self.random.nextInt(min,max)
        self.level.s2_shuffleSeed=self.random.nextInt(min,max)
        self.level.s2t_shuffle2Times=self.random.nextInt(min,max)



    def encryptLevel(self):
        msg=self.level.inputMsg
        if self.streamConverter:
            msg=self.streamConverter.convertInput(msg)
        print("MSG: ")
        print(msg)
        Bp=self.generatePerMsgWindowSetting(self.baseMachine)
        print("Bp: ")
        print(Bp)
        EBp=self.encryptSequence(Bp,self.baseMachine,self.level.o_PerMsgBpEncTimes)
        print("EBp: ")
        print(EBp)
        Emsg=EBp+self.encryptSequence(msg,self.baseMachine,self.level.p_BpEncTimes,Bp)
        print("Emsg: ")
        print(Emsg)
        SEmsg=self.shuffler.shuffleSeq(Emsg,self.level.s1_shuffleSeed)
        print("SEmsg: ")
        print(SEmsg)
        x=self.encryptSequence(SEmsg,self.baseMachine,self.level.i_firstBsEncTimes)
        print("x: ")
        print(x)
        y=self.encryptSequence(x,self.levelMachine,self.level.j_firstMsEncTimes)
        print("y: ")
        print(y)
        Mp=self.generatePerMsgWindowSetting(self.levelMachine)
        print("Mp: ")
        print(Mp)
        EMp=self.encryptSequence(Mp,self.levelMachine,self.level.k_PerMsgMsEncTimes)
        print("EMp: ")
        print(EMp)
        M0=self.encryptSequence(y,self.levelMachine,self.level.l_MmpEncTimes,Mp)
        print("M0: ")
        print(M0)
        W=EMp+M0
        print("W: ")
        print(W)
        S=self.shuffler.shuffleSeq(W,self.level.s2_shuffleSeed)
        print("S: ")
        print(S)
        R=self.encryptSequence(S,self.levelMachine,self.level.m_secondMsEncTimes)
        print("R: ")
        print(R)
        E=self.encryptSequence(R,self.baseMachine,self.level.n_secondBsEncTimes)
        print("E: ")
        print(E)

        self.level.outputMsg=E
        print("Encrpytion:")
        print(E)
        if self.streamConverter:
            self.level.outputMsg=self.streamConverter.convertOutput(E)
        return self.level


    def encryptSequence(self,seq,machine,times=1,displayStg=None):
        result=[]
        preEncryptionStg=machine.getMachineSettings()
        print("currnetMachine stg:")
        preEncryptionStg.print()
        if displayStg:
            machine.adjustWindowDisplay(displayStg)

        for c in seq:
            result.append(machine.processKeyPress(c))
        machine.adjustMachineSettings(preEncryptionStg)
        return result




    def generatePerMsgWindowSetting(self,mc):
        result=[]
        for i in range(mc.getCipherRotorsCount()):
            selectedOffset=self.random.sample(range(mc.getCipherRotorsSize()),1)[0]
            result.append(selectedOffset)
        return result
