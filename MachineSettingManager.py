from MachineSettingsMemento import MachineSettingsMemento
from RandomGenerator import RandomGenerator
from PlugBoard import PlugBoard
from MapperSwitch import MapperSwitch
from Wiring import Wiring
from CharIndexMap import CharIndexMap


class MachineSettingManager(object):
    def __init__(self,seed=None):
        self.random=RandomGenerator(seed)

    @classmethod
    def generateDefaultSettingsForMachine(self,mc):
        memento=MachineSettingsMemento()

        memento.cipherRotorStg=self.generateDefaultSettingsForRotorStock(mc.cipherRotorStockMap)
        memento.plugboardStg["wiring"]=[]

        memento.swappingRotorStg=self.generateDefaultSettingsForRotorStock(mc.swappingRotorStockMap)

        memento.activeSwapSignals={"CYCLE_STEP":1,"SIGNALS":[0]}


        return memento


    @classmethod
    def generateDefaultSettingsForRotorStock(self,rotorStockMap):
        result={}
        result["ORDER"]=[]
        result["OFFSET"]=[]
        for rId in rotorStockMap.keys():
            result["ORDER"].append(rId)
            result["OFFSET"].append(0)
        return result
    def generateRandomSettingsForRotorStock(self,rotorStockMap):
        result={}
        result["ORDER"]=[]
        result["OFFSET"]=[]
        rotorStockIds=list(rotorStockMap.keys())
        k=self.random.nextInt(len(rotorStockIds)*3//4,len(rotorStockIds))
        #must select at least one
        if k==0:
            k=1
        selectedRotorNumbers=self.random.sample(rotorStockIds,k)
        rotorSize=rotorStockMap[rotorStockIds[0]].size
        for rId in selectedRotorNumbers:
            result["ORDER"].append(rId)
            result["OFFSET"].append(self.random.nextInt(0,rotorSize))
        return result

    def generateRandomSettingsForMachine(self,mc):
        memento=MachineSettingsMemento()

        memento.cipherRotorStg=self.generateRandomSettingsForRotorStock(mc.cipherRotorStockMap)
        memento.plugboardStg=self.generateRandomWiringForPlugBoard()

        memento.swappingRotorStg=self.generateRandomSettingsForRotorStock(mc.swappingRotorStockMap)

        memento.activeSwapSignals=self.generateRandomActiveSwapSignalStg(mc)

        return memento
    def generateRandomActiveSwapSignalStg(self,mc):
        cycleStep=self.random.nextInt()
        swapRotorSize=next(iter (mc.swappingRotorStockMap.values())).size
        k=self.random.nextInt(1,swapRotorSize//4)
        signals=self.random.sample(range(swapRotorSize),k)
        result={"CYCLE_STEP":cycleStep,"SIGNALS":signals}
        return result
    def generateRandomWiringForPlugBoard(self):
        result={"wiring":{}}
        k=self.random.nextInt(0,CharIndexMap.getRangeSize()//2)
        totalRange=list(CharIndexMap.getRange())
        for i in range(k):
            selctedPair=self.random.sample(totalRange,2)
            fromPin=selctedPair[0]
            toPin=selctedPair[1]
            totalRange.remove(fromPin)
            totalRange.remove(toPin)
            result["wiring"][fromPin]=[toPin]
            result["wiring"][toPin]=[fromPin]
        return result

    @classmethod
    def backupMachineSettings(cls,mc):
        if not mc.settingsReady:
            raise Exception("Can't take settings backup, this machine has no settings!!")
        memento=MachineSettingsMemento()
        memento.cipherRotorStg=MachineSettingManager.extractRotorSettingsFromRotorList(mc.cipherRotorIdList,mc.cipherRotorStockMap)
        memento.plugboardStg={"wiring":mc.plugboard.wiring.getAsMap()}
        memento.swappingRotorStg=MachineSettingManager.extractRotorSettingsFromRotorList(mc.swapRotorsIdList,mc.swappingRotorStockMap)
        memento.activeSwapSignals={"CYCLE_STEP":mc.swapActiveSignalsCycleStep,"SIGNALS":mc.swapActiveSignals}
        return memento
    @classmethod
    def extractRotorSettingsFromRotorList(self,rotorIdList,rotorStockMap):
        result={}
        result["ORDER"]=[]
        result["OFFSET"]=[]
        for rId in rotorIdList:
            result["ORDER"].append(rId)
            result["OFFSET"].append(rotorStockMap[rId].offset)
        return result

    @classmethod
    def applyMachineSettings(self,mc,settingsMemento):
        if not settingsMemento:
            raise Exception("Settings not found to ajdust !!")
        mc.rotorIdList=[]
        index=0
        for rId in settingsMemento.cipherRotorStg["ORDER"]:
            mc.rotorIdList.append(rId)
            mc.cipherRotorStockMap[rId].offset=settingsMemento.cipherRotorStg["OFFSET"][index]
            index+=1

        mc.plugboard=PlugBoard(Wiring(settingsMemento.plugboardStg["wiring"]))

        mc.swapActiveSignals=settingsMemento.activeSwapSignals["SIGNALS"]
        mc.swapActiveSignalsCycleStep=settingsMemento.activeSwapSignals["CYCLE_STEP"]

        mc.swapRotorsIdList=[]
        index=0
        for rId in settingsMemento.swappingRotorStg["ORDER"]:
            mc.swapRotorsIdList.append(rId)
            mc.swappingRotorStockMap[rId].offset=settingsMemento.swappingRotorStg["OFFSET"][index]

        mc.settingsReady=True


    @classmethod
    def restoreMachinneSettings(cls,mc,memento):
        raise Exception("Unimplemented operation")
        pass
