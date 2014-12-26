from PlugBoard import PlugBoard
from Rotor import Rotor
from Reflector import Reflector
from CharIndexMap import CharIndexMap
from Wiring import Wiring
from RandomGenerator import RandomGenerator
from MachineSettingsMemento import MachineSettingsMemento
from MachineSettingManager import MachineSettingManager

class ModernEnigma:
    def __init__(self,rotorStockList,reflector,plugboard,l1SwappingRotorStockList,l2SwappingRotorStockList,l1l2SeparatorSwitch):
        self.settingsReady=False
        self.rotorStockList=rotorStockList
        self.rotorsStockMap={}
        for rotorStock in rotorStockList:
            self.rotorsStockMap[rotorStock.id]=rotorStock
        self.rotorList=[]
        self.reflector=reflector
        self.plugboard=plugboard
        """swapping settings"""
        self.l1SwappingRotorStockList=l1SwappingRotorStockList
        self.l2SwappingRotorStockList=l2SwappingRotorStockList
        self.l1l2SeparatorSwitch=l1l2SeparatorSwitch
        self.swapRotorsLevel1=[]
        self.swapRotorsLevel2=[]
        self.swapActiveSignals=[]
        self.swapActiveSignalsCycleStep=0
        self.l2CipherMapper=None
        self.cyclePeriod=None


    def adjustMachineSettings(self,settingsMemento=None):
        if not settingsMemento:
            settingsMemento=MachineSettingManager.generateDefaultSettingsForMachine(self)
        MachineSettingManager.applyMachineSettings(self,settingsMemento)

    def processKeyPress(self,indexIn):
        if not self.settingsReady :
            raise Exception("Settings are not set for this machine!!")
        lastOut=self.plugboard.signalIn(indexIn)
        inputPins=[lastOut]
        resultPins=self.applyActivePins(self.rotorList,inputPins)

        lastReverseIn=self.reflector.signalIn(resultPins[0])

        resultPins=self.applyActivePinsReversed(self.rotorList,[lastReverseIn])
        output=self.plugboard.reverseSignal(resultPins[0])

        self.processStepping(self.rotorList)

        # self.processRotorSwapping(lastOut)

        return output

    def processRotorSwapping(self,indexIn):
        activePins=self.swapActiveSignals
        swapLevel1Result=self.applyActivePins(self.swapRotorsLevel1,activePins)
        swapLevel2Input=self.applyMappingActivePins(self.l1l2SeparatorSwitch,swapLevel1Result)
        swapLevel2Result=self.applyActivePins(self.swapRotorsLevel2,swapLevel2Input)
        swapResult=self.applyMappingActivePins(self.l2CipherMapper,swapLevel2Result)

        self.swapRotors(self.rotorList,swapResult)

        self.processStepping(self.swapRotorsLevel1)
        self.processStepping(self.swapRotorsLevel2)

        #shift swappingSignalsByStep
        self.processActiveSwapSignalsCycleStep()

    def swap(self,rotorList,i,j):
        tmp=rotorList[i]
        rotorList[i]=rotorList[j]
        rotorList[j]=tmp

    def swapRotors(self,rotorList,swapIndexList):
        for index in swapIndexList:
            if index==0 or index==len(rotorList)-1:
                self.swap(rotorList,0,len(rotorList)-1)
                continue
            self.swap(rotorList,index,(3*index)%len(rotorList))

    def processActiveSwapSignalsCycleStep(self):
        result=[]
        for s in self.swapActiveSignals:
            newSignalIndex=(s+self.swapActiveSignalsCycleStep) %self.swapRotorsLevel1[0].size
            result.append(newSignalIndex)

        self.swapActiveSignals=result


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

    def getCipherRotorsCount(self):
        return len(self.rotorList)
    def getCipherRotorsSize(self):
        return self.rotorList[0].size

    def adjustWindowDisplay(self,windowSetting):
        for i in range(len(windowSetting)):
            self.rotorList[i].adjustDisplay(windowSetting[i])


    def getMachineSettings(self):
        return MachineSettingManager.backupMachineSettings(self)

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







