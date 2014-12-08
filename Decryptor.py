from ModernEnigma import ModernEnigma
from CharIndexMap import CharIndexMap

class Decryptor(object):
    def __init__(self,machine,options=None):
        self.machine=machine
        self.options=options
        self.preDecryptionStg=machine.getMachineSettings()
    def decryptMsg(self,msg):
#machine displat settings is no of rotors

        #decrypt the perMSgStg with current base settings
        perMsgStg=""
        result=""
        for i in range(len(self.machine.rotorList)):
            perMsgStg+=self.machine.processKeyPress(msg[i])
        #adjust window to new perMsgStg
        self.machine.adjustWindowDisplay(perMsgStg)
        #now encrypt msg
        for c in msg[len(perMsgStg):len(msg)]:
            result+=self.machine.processKeyPress(c)

        # msg=self.replaceSpaceCharInMsg(msg)
        self.restoreMachine()
        return result

    def restoreMachine(self):
        self.machine.adjustMachineSettings(self.preDecryptionStg)

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
        ran=Random()
        randomRange= sorted(CharIndexMap.getRange(), key=lambda k: ran.random())
        result=""
        for c in randomRange:
            result+=c
        return c


