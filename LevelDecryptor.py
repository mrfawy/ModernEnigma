from RandomGenerator import RandomGenerator
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
        self.random=random
        if random==None:
            self.random=RandomGenerator()
        self.shuffler=Shuffler()

    def decryptPhase(self,id,machine1,machine2,seq):
        x=self.encryptSequence(seq,machine2,self.level.l[id])
        SEMsg=self.encryptSequence(x,machine1,self.level.k[id])
        EMsg=self.shuffler.deshuffleSeq(SEMsg,self.level.s[id])
        EM1p=EMsg[0:len(machine1.rotorList)]
        Msg_M1p=EMsg[len(machine1.rotorList)::]
        M1p=self.encryptSequence(EM1p,machine2,self.level.i[id])
        Msg=self.encryptSequence(Msg_M1p,machine1,self.level.j[id],M1p)

        return Msg



    def decryptLevel(self,verbose=False):

        E=self.level.outputMsg
        if self.streamConverter:
            E=self.streamConverter.convertInput(E)

        phaseDecOut=self.decryptPhase(1,self.levelMachine,self.baseMachine,E)
        phaseDecOut=self.decryptPhase(0,self.baseMachine,self.levelMachine,phaseDecOut)
        self.level.inputMsg=phaseDecOut
        if self.streamConverter:
            self.level.inputMsg=self.streamConverter.convertInput(msg)
        return self.level



