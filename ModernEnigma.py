from Plugboard import PlugBoard
from Rotor import Rotor
from Reflector import Reflector
from CharIndexMap import CharIndexMap
from Wiring import Wiring
import fixedSettings
import random

class ModernEnigma:
    def __init__(self,rotorStockList,reflector,plugboard,fixedSwapSignals,l1SwappingRotorStockList,l2SwappingRotorStockList,l1l2SeparatorSwitch,l2CipherMapper,initSetting=None):

        self.rotorStockList=rotorStockList
        self.rotorsStockMap={}
        for rotorStock in rotorStockList:
            self.rotorsStockMap[str(rotorStock.id)]=rotorStock
        self.rotorList=[]
        self.cyclePeriod=0
        self.reflector=reflector
        self.plugboard=plugboard
        """swapping settings"""
        self.l1SwappingRotorStockList=l1SwappingRotorStockList
        self.l2SwappingRotorStockList=l2SwappingRotorStockList
        self.l1l2SeparatorSwitch=l1l2SeparatorSwitch
        self.l2CipherMapper=l2CipherMapper
        self.swapRotorsLevel1=[]
        self.swapRotorsLevel2=[]
        self.baseSwapActiveChars=[]
        for c in fixedSwapSignals:
            self.baseSwapActiveChars.append(c)

        if initSetting:
            self.adjustMachineSettings(initSetting)
        else:
            self.adjustDefaultSettings()

    def adjustDefaultSettings(self):
        for rotorStock in self.rotorStockList:
            self.rotorList.append(rotorStock)
        self.adjustDefaultSwappingRotorSettings()

    def adjustDefaultSwappingRotorSettings(self):
        """Load L1 , L2 in order from stock ,Create default Separator
        Create Default Mapping from L2 to Cipher rotors"""
        self.swapRotorsLevel1=[]
        self.swapRotorsLevel2=[]
        for l1Rotor in self.l1SwappingRotorStockList:
            l1Rotor.offset=0
            self.swapRotorsLevel1.append(l1Rotor)
        for l2Rotor in self.l2SwappingRotorStockList:
            l2Rotor.offset=0
            self.swapRotorsLevel2.append(l2Rotor)

    #fromat for setting line
    #2 digitID rotor order for selected rotor set |1 char for offset |2 chars for each plugboard pair |(optional) dynamic inmsg  conf change rules
    def adjustMachineSettings(self,settings):
        """WILL BE REMOVED AFTER SETTING FORMAT IS DONE FOR SWAPPING"""
        self.adjustDefaultSwappingRotorSettings()
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
        resultPins=self.applyActivePins(self.rotorList,[lastOut])

        lastReverseIn=self.reflector.signalIn(resultPins[0])

        resultPins=self.applyActivePinsReversed(self.rotorList,[lastReverseIn])
        output=self.plugboard.reverseSignal(resultPins[0])

        self.processStepping(self.rotorList)

        self.processRotorSwapping(lastOut)

        return CharIndexMap.indexToChar(output)

    def processRotorSwapping(self,indexIn):
        lastout=indexIn
        activePins=[]
        for c in self.baseSwapActiveChars:
            activePins.append(CharIndexMap.charToIndex(c))
        if lastout not in activePins:
            activePins.append(lastout)

        swapLevel1Result=self.applyActivePins(self.swapRotorsLevel1,activePins)
        swapLevel2Input=self.applyMappingActivePins(self.l1l2SeparatorSwitch,swapLevel1Result)
        swapLevel2Result=self.applyActivePins(self.swapRotorsLevel2,swapLevel2Input)
        swapResult=self.applyMappingActivePins(self.l2CipherMapper,swapLevel2Result)

        self.swapRotors(self.rotorList,swapResult)

        self.processStepping(self.swapRotorsLevel1)
        self.processStepping(self.swapRotorsLevel2)

    def swap(self,rotorList,i,j):
        tmp=rotorList[i]
        rotorList[i]=rotorList[j]
        rotorList[j]=tmp

    def swapRotors(self,rotorList,swapIndexList):
        for index in swapIndexList:
            self.swap(rotorList,index,(index+1)%len(rotorList))

    def applyActivePins(self,rotors,pins):
        resultPins=[]
        for pin in pins:
            lastout=pin
            for rotor in rotors:
                lastout=rotor.signalIn(lastout)
            if lastout not in resultPins:
                resultPins.append(lastout)
        return resultPins
    def applyMappingActivePins(self,mapper,pins):
        resultPins=[]
        for pin in pins:
           outputs=mapper.signalIn(pin)
           for o in outputs:
                if o not in resultPins:
                    resultPins.append(o)
        return resultPins

    def applyActivePinsReversed(self,rotors,pins):
        resultPins=[]
        for pin in pins:
            lastout=pin
            for rotor in reversed(rotors):
                lastout=rotor.reverseSignal(lastout)
            if lastout not in resultPins:
                resultPins.append(lastout)
        return resultPins

    def processStepping(self,rotors):
        notchFlag=False
        for i  in range(len(rotors)) :
            rotor=rotors[i]
            if i==0:
                notchFlag=rotor.rotate()
                continue
            if notchFlag:
                notchFlag=rotor.rotate()

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
        """settings format 2chars of rotorID  of right order | 1  char each of win display |plugboard settings|swappingSettings| (optional) cycle"""
        """swapping Settings : 2Chars L1RotorID of right order|1 char of L1Rotor offset|2 chars ordered  L2RotorID |1 char L2Rotors offset|L2toCipher rotors mapping reversed from N rotors to K (L2 rotor size) """
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

    def printMachineInformation(self):
        info="""Mahcine Information:
                Cipher:
                    Current Active Rotors:{0} / {1}
                Swapping:
                    L1 rotor count :{2} , Size : {3}
                    L2 rotor Count: {4}, size : {5}"""
        info=info.format(len(self.rotorList),len(self.rotorStockList),len(self.l1SwappingRotorStockList),str(self.swapRotorsLevel1[0].size),len(self.l2SwappingRotorStockList),str(self.swapRotorsLevel2[0].size))
        print (info)







