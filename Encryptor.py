from ModernEnigma import ModernEnigma
from CharIndexMap import CharIndexMap
from random import Random

class Encryptor(object):
    def __init__(self,machine,options=None):
        self.machine=machine
        self.options=options
        self.preEncryptionStg=machine.getMachineSettings()
        self.random=Random()
    def encryptMsg(self,msg):
        msg=self.replaceSpaceCharInMsg(msg)
        perMsgStg=self.generatePerMsgWindowSetting()
        #encrypt the perMSgStg with current base settings
        result=""
        for c in perMsgStg:
            result+=self.machine.processKeyPress(c)
        self.machine.adjustWindowDisplay(perMsgStg)
        #now encrypt msg
        for c in msg:
            result+=self.machine.processKeyPress(c)
        self.restoreMachine()
        return result

    def restoreMachine(self):
        self.machine.adjustMachineSettings(self.preEncryptionStg)

    def replaceSpaceCharInMsg(self,msg):
        rplChar= self.random.sample(CharIndexMap.getRange(),1)
        result=""
        for i in range(len(msg)):
            if msg[i]==" ":
               result+=rplChar
            else:
                result+=msg[i]
        return result
    def generatePerMsgWindowSetting(self):
        randomRange= sorted(CharIndexMap.getRange(), key=lambda k: self.random.random())
        result=""
        for i in range(len(self.machine.rotorList)):
            result+=randomRange[i]
        print("PER MSG:"+result)
        return result


