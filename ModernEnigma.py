from Plugboard import PlugBoard
from Rotor import Rotor
from Reflector import Reflector
from CharIndexMap import CharIndexMap
from Wiring import Wiring
import fixedSettings

class ModernEnigma:
    def __init__(self,rotorStockList,reflector,plugboard,initSetting=None):
        self.rotorStockList=rotorStockList
        self.rotorsStockMap={}
        for rotorStock in rotorStockList:
            self.rotorsStockMap[rotorStock.id]=rotorStock
        self.rotorList=[]
        self.reflector=reflector
        self.plugboard=plugboard
        if initSetting:
            self.adjustMachineSettings(initSetting)
        else:
            self.adjustDefaultSettings()

    def adjustDefaultSettings(self):
        for rotorStock in self.rotorStockList:
            self.rotorList.append(rotorStock)

    #fromat for setting line
    #2 digitID rotor order for selected rotor set |1 char for offset |2 chars for each plugboard pair |(optional) dynamic inmsg  conf change rules
    def adjustMachineSettings(self,settings):
        settingsParts=settings.split('|')
        rotorOrderStg=settingsParts[0]
        rotorOffsetStg=settingsParts[1]
        plugboardStg=settingsParts[2]

        i=len(rotorOrderStg)
        while i>0:
            rotorId=rotorOrderStg[i-2:i-1]
            self.rotorList.append(self.rotorsStockMap[rotorId])
            i-=2
        j=0
        for offsetChar in reversed(rotorOffsetStg):
            self.rotorList[j].adjustDisplay(offsetChar)
            j+=1
        #setting plugboard
        self.plugboard=Plugboard(plugboardStg)



    def processKeyPress(self,char):
        indexIn=CharIndexMap.charToIndex(char)
        # print("indexIn"+str(indexIn))
        lastOut=self.plugboard.signalIn(indexIn)
        # print("plug"+str(lastOut))
        for rotor in self.rotorList:
            lastOut=rotor.signalIn(lastOut)
            # print("rotorIn"+str(lastOut))
        lastReverseIn=self.reflector.signalIn(lastOut)
        # print("reflectorRev"+str(lastReverseIn))
        for rotor in reversed(self.rotorList):
            lastReverseIn=rotor.reverseSignal(lastReverseIn)
            # print("rotorReve"+str(lastReverseIn))
        output=self.plugboard.reverseSignal(lastReverseIn)
        # print("plugRev"+str(output))

        notchFlag=False
        for i  in range(len(self.rotorList)) :
            rotor=self.rotorList[i]
            if i==0:
                notchFlag=rotor.rotate()
                continue
            if notchFlag:
                notchFlag=rotor.rotate()
        return CharIndexMap.indexToChar(output)

    def getWindowDisplay(self):
        result="Window||"
        for rotor in reversed(self.rotorList):
            result+=rotor.getDisplay()+" "
        return result

    def getMachineSettings(self):
        #settings format 2chars of rotorID  of right order | 1  char each of win display |plugboard settings| (optional) cycle
        rotorOrderStg=""
        rotorOffsetStg=""
        for rotor in reversed(self.rotorList):
            rotorOrderStg+=str(rotor.id) if len(str(rotor.id))>1 else "0"+str(rotor.id)
            rotorOffsetStg+=rotor.getDisplay()

        return rotorOrderStg+"|"+rotorOffsetStg+"|"+self.plugboard.getSettings()



#
# RI=fixedSettings.ROTORS["I"]
# RII=fixedSettings.ROTORS["II"]
# RIII=fixedSettings.ROTORS["III"]
# REF_B=fixedSettings.REFLECTORS["B"]
#
# r0=Rotor(Wiring(RI['wiring']),RI['stepping'])
# r1=Rotor(Wiring(RII['wiring']),RII['stepping'])
# r2=Rotor(Wiring(RIII['wiring']),RIII['stepping'])
# r3=Rotor(Wiring(RIII['wiring']),RIII['stepping'])
# r4=Rotor(Wiring(RIII['wiring']),RIII['stepping'])
# r5=Rotor(Wiring(RIII['wiring']),RIII['stepping'])
# reflector=Reflector(Wiring(REF_B))
#
#
# plugboard=PlugBoard(Wiring(RI["wiring"]))
# mc=ModernEnigma([r0,r1,r2,r3,r4,r5],reflector,plugboard)
# MSG="ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
# MSG="VSYAJCSMNTOAGHIAHYZYEICZSUPYPVODZVKUCGKYXJBPVJWTLGDK"
# encMsg=""
# for c in MSG:
#     encMsg+=mc.processKeyPress(c)
# print("result: "+encMsg)
# print (mc.getWindowDisplay())
#
# # import pdb; pdb.set_trace()
