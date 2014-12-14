from Plugboard import PlugBoard
from Rotor import Rotor
from Reflector import Reflector
from CharIndexMap import CharIndexMap
from Wiring import Wiring
import fixedSettings
import random

class ModernEnigma:
    def __init__(self,rotorStockList,reflector,plugboard,initSetting=None):
        self.rotorStockList=rotorStockList
        self.rotorsStockMap={}
        for rotorStock in rotorStockList:
            self.rotorsStockMap[str(rotorStock.id)]=rotorStock
        self.rotorList=[]
        self.cyclePeriod=0
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

        self.rotorList=[]

        i=len(rotorOrderStg)
        while i>0:
            rotorId=str(int(rotorOrderStg[i-2:i]))
            self.rotorList.append(self.rotorsStockMap[rotorId])
            i-=2
        j=0
        for offsetChar in reversed(rotorOffsetStg):
            self.rotorList[j].adjustDisplay(offsetChar)
            j+=1
        #setting plugboard
        if len(settingsParts)>2:
            plugboardStg=settingsParts[2]
            self.plugboard=PlugBoard(plugboardStg)
        #settingCyclePeriod
        if len(settingsParts)>3:
            self.cyclePeriod=int(settingsParts[3])




    def processKeyPress(self,char):
        indexIn=CharIndexMap.charToIndex(char)
        lastOut=self.plugboard.signalIn(indexIn)
        for rotor in self.rotorList:
            lastOut=rotor.signalIn(lastOut)
        lastReverseIn=self.reflector.signalIn(lastOut)
        for rotor in reversed(self.rotorList):
            lastReverseIn=rotor.reverseSignal(lastReverseIn)
        output=self.plugboard.reverseSignal(lastReverseIn)

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
    def adjustWindowDisplay(self,windowSetting):
        #reversed string order
        i=len(windowSetting)-1
        for c in windowSetting[::-1]:
            self.rotorList[i].adjustDisplay(c)
            i-=1


    def getMachineSettings(self):
        #settings format 2chars of rotorID  of right order | 1  char each of win display |plugboard settings| (optional) cycle
        rotorOrderStg=""
        rotorOffsetStg=""
        for rotor in reversed(self.rotorList):
            rotorOrderStg+=str(rotor.id) if len(str(rotor.id))>1 else "0"+str(rotor.id)
            rotorOffsetStg+=rotor.getDisplay()

        result= rotorOrderStg+"|"+rotorOffsetStg+"|"+self.plugboard.getSettings()+"|"+str(self.cyclePeriod)
        return result

    def cycleRotorsForward(self):
        lastRotor=self.rotorList[-1]
        for i in range(len(self.rotorList)-1,0,-1):
            self.rotorList[i]=self.rotorList[i-1]
        self.rotorList[0]=lastRotor

    def cycleRotorsBackward(self):
        firstRotor=self.rotorList[0]
        for i in range(0,len(self.rotorList)-1):
            self.rotorList[i]=self.rotorList[i+1]
        self.rotorList[-1]=firstRotor






