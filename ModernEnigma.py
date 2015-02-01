from PlugBoard import PlugBoard
from Rotor import Rotor
from Reflector import Reflector
from CharIndexMap import CharIndexMap
from Wiring import Wiring
from RandomGenerator import RandomGenerator
from MachineSettingsMemento import MachineSettingsMemento
from MachineSettingManager import MachineSettingManager
from Util import Util
from Shuffler import Shuffler
import copy

class ModernEnigma:
    def __init__(self,cipherRotorStockMap,reflector,plugboard,swappingRotorStockMap):
        self.settingsReady=False
        self.cipherRotorStockMap=cipherRotorStockMap
        self.cipherRotorIdList=[]
        self.reflector=reflector
        self.plugboard=plugboard
        """swapping settings"""
        self.swappingRotorStockMap=swappingRotorStockMap
        self.swapRotorsIdList=[]
        self.swapActiveSignals=[]
        self.swapSalt=None
        self.swapActiveSignalsCycleStep=0


    def adjustMachineSettings(self,settingsMemento=None):
        if not settingsMemento:
            settingsMemento=MachineSettingManager.generateDefaultSettingsForMachine(self)
        MachineSettingManager.applyMachineSettings(self,settingsMemento)

    def processKeyListPress(self,indexInList):
        if not self.settingsReady :
            raise Exception("Settings are not set for this machine!!")
        lastOut=self.plugboard.signalIn(indexInList)
        inputPins=lastOut
        resultPins=self.applyActivePins(self.cipherRotorIdList,self.cipherRotorStockMap,inputPins)

        lastReverseIn=self.reflector.signalIn(resultPins)

        resultPins=self.applyActivePinsReversed(self.cipherRotorIdList,self.cipherRotorStockMap,lastReverseIn)
        output=self.plugboard.reverseSignal(resultPins)

        self.processStepping(self.cipherRotorIdList,self.cipherRotorStockMap)

        self.processRotorSwapping()

        return output

    def processRotorSwapping(self):
        activePins=self.swapActiveSignals
        swapResult=self.applyActivePins(self.swapRotorsIdList,self.swappingRotorStockMap,activePins)

        swapSeed=self.swapSalt+Util.seqToStr(swapResult)
        self.cipherRotorIdList=Shuffler.shuffleSeq(self.cipherRotorIdList,swapSeed)

        self.processStepping(self.swapRotorsIdList,self.swappingRotorStockMap)

        #shift swappingSignalsByStep
        self.processActiveSwapSignalsCycleStep()



    def processActiveSwapSignalsCycleStep(self):
        result=[]
        for s in self.swapActiveSignals:
            swapRotorSize=self.swappingRotorStockMap[self.swapRotorsIdList[0]].size
            newSignalIndex=(s+self.swapActiveSignalsCycleStep) %swapRotorSize
            result.append(newSignalIndex)

        self.swapActiveSignals=result


    def applyActivePins(self,rotorIdList,rotorStockMap,pins):
        lastout=pins
        for rId in rotorIdList:
            rotor=rotorStockMap[rId]
            lastout=rotor.signalIn(lastout)
        return lastout

    def applyActivePinsReversed(self,rotorIdList,rotorStockMap,pins):
        lastout=pins
        for rId in reversed(rotorIdList):
            rotor=rotorStockMap[rId]
            lastout=rotor.reverseSignal(lastout)
        return lastout

    def processStepping(self,rotorIdList,rotorStockMap):
        notchFlag=False
        index=0
        for rId  in rotorIdList :
            rotor=rotorStockMap[rId]
            if index==0:
                notchFlag=rotor.rotate()
                index+=1
                continue
            if notchFlag:
                notchFlag=rotor.rotate()

    def getCipherRotorsCount(self):
        return len(self.cipherRotorIdList)

    def getCipherRotorsSize(self):
        return self.cipherRotorStockMap[self.cipherRotorIdList[0]].size

    def adjustWindowDisplay(self,windowSetting):
        if(len(windowSetting)!=self.getCipherRotorsCount()):
            raise ("Invalid window setting !!, size doesn't match with cipher rotor count ")
        for i in range(self.getCipherRotorsCount()):
            rotor=self.cipherRotorStockMap[self.cipherRotorIdList[i]]
            rotor.adjustDisplay(windowSetting[i])


    def getMachineSettings(self):
        return MachineSettingManager.backupMachineSettings(self)


    def printMachineInformation(self):
        raise ("Not implemented Feature")

    def clone(self):
        return copy.deepcopy(self)



