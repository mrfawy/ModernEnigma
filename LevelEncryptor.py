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
        min=3
        max=16
        self.level.i[0]=self.random.nextInt(min,max)
        self.level.i[1]=self.random.nextInt(min,max)
        self.level.j[0]=self.random.nextInt(min,max)
        self.level.j[1]=self.random.nextInt(min,max)
        self.level.k[0]=self.random.nextInt(min,max)
        self.level.k[1]=self.random.nextInt(min,max)
        self.level.l[0]=self.random.nextInt(min,max)
        self.level.l[1]=self.random.nextInt(min,max)
        self.level.s[0]=self.random.nextInt(min,max)
        self.level.s[1]=self.random.nextInt(min,max)
        self.level.st[0]=self.random.nextInt(min,max)
        self.level.st[1]=self.random.nextInt(min,max)

    def encryptPhase(self,id,machine1,machine2,seq):
        M1p=self.generatePerMsgWindowSetting(machine1)
        EM1p=self.encryptSequence(M1p,machine2,self.level.i[id])
        Msg_M1p=self.encryptSequence(seq,machine1,self.level.j[id],M1p)
        EMsg=EM1p+Msg_M1p
        SEMsg=self.shuffler.shuffleSeq(EMsg,self.level.s[id])
        x=self.encryptSequence(SEMsg,machine1,self.level.k[id])
        y=self.encryptSequence(x,machine2,self.level.l[id])
        return y


    def encryptLevel(self,verbose=False):
        seq=self.level.inputMsg
        if self.streamConverter:
            seq=self.streamConverter.convertInput(msg)

        phaseEncOut=self.encryptPhase(0,self.baseMachine,self.levelMachine,seq)
        phaseEncOut=self.encryptPhase(1,self.levelMachine,self.baseMachine,phaseEncOut)
        self.level.outputMsg=phaseEncOut
        if self.streamConverter:
            self.level.outputMsg=self.streamConverter.convertOutput(E)
        return self.level


    def encryptSequence(self,seq,machine,times=1,displayStg=None):
        result=[]
        preEncryptionStg=machine.getMachineSettings()
        if displayStg:
            machine.adjustWindowDisplay(displayStg)

        result=seq
        for t in range(times):
            result=self.processSeq(result,machine)

        machine.adjustMachineSettings(preEncryptionStg)
        return result

    def processSeq(self,seq,machine):
        result=[]
        for c in seq:
            result.append(machine.processKeyPress(c))
        return result



    def generatePerMsgWindowSetting(self,mc):
        result=[]
        for i in range(mc.getCipherRotorsCount()):
            selectedOffset=self.random.sample(range(mc.getCipherRotorsSize()),1)[0]
            result.append(selectedOffset)
        return result
