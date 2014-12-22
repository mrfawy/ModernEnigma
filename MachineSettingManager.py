from MachineSettingsMemento import MachineSettingsMemento
from RandomGenerator import RandomGenerator
from PlugBoard import PlugBoard
from MapperSwitch import MapperSwitch
from Wiring import Wiring


class MachineSettingManager(object):
    def __init__(self,random=None):
        if not random:
            self.random=RandomGenerator()

    @classmethod
    def generateDefaultSettingsForMachine(self,mc):
        memento=MachineSettingsMemento()

        memento.cipherRotorStg=self.generateDefaultSettingsForRotorStock(mc.rotorStockList)
        memento.plugboardStg["wiring"]=[]

        memento.swappingL1Stg=self.generateDefaultSettingsForRotorStock(mc.l1SwappingRotorStockList)
        memento.swappingL2Stg=self.generateDefaultSettingsForRotorStock(mc.l2SwappingRotorStockList)

        memento.L1L2MapperStg["OFFSET"]=0
        memento.activeSwapSignals={"CYCLE_STEP":1,"SIGNALS":[0]}
        memento.cyclePeriod=None

        fromRange=range(mc.l2SwappingRotorStockList[0].size)
        toRange=range(len(mc.rotorStockList))
        memento.L2CipherMapperStg=self.gererateDefaultSettingsForMapper(fromRange,toRange)

        return memento

    """ map each pin in from Range to ToRange , cover the other end as well"""
    @classmethod
    def gererateDefaultSettingsForMapper(self,fromRange,toRange):
        result={"wiring":{}}
        coveredTo=[]
        wiringMap=result["wiring"]
        lastToIndex=0
        for frompin in fromRange:
            wiringMap[frompin]=[]
            wiringMap[frompin].append(lastToIndex)
            if lastToIndex not in coveredTo:
                coveredTo.append(lastToIndex)
            lastToIndex=(lastToIndex+1)%len(toRange)

        lastFromIndex=0
        for toPin in toRange:
            if toPin not in coveredTo:
                wiringMap[lastFromIndex].append(toPin)
            lastFromIndex=(lastFromIndex+1)%len(fromRange)

        return result

    @classmethod
    def generateDefaultSettingsForRotorStock(self,rotorStock):
        result={}
        result["ORDER"]=[]
        result["OFFSET"]=[]
        for rotor in rotorStock:
            result["ORDER"].append(int(rotor.id))
            result["OFFSET"].append(0)
        return result
    def generateRandomSettingsForMachine(self):
        raise Exception("Unimplemented operation")

    @classmethod
    def backupMachineSettings(cls,mc):
        if not mc.settingsReady:
            raise Exception("Can't take settings backup, this machine has no settings!!")
        memento=MachineSettingsMemento()
        memento.cipherRotorStg=MachineSettingManager.extractRotorSettingsFromRotorList(mc.rotorList)
        memento.plugboardStg={"wiring":mc.plugboard.wiring.extractAsMap()}
        memento.swappingL1Stg=MachineSettingManager.extractRotorSettingsFromRotorList(mc.swapRotorsLevel1)
        memento.swappingL2Stg=MachineSettingManager.extractRotorSettingsFromRotorList(mc.swapRotorsLevel2)
        memento.L1L2MapperStg={"OFFSET":mc.l1l2SeparatorSwitch.offset}
        memento.activeSwapSignals={"CYCLE_STEP":mc.swapActiveSignalsCycleStep,"SIGNALS":mc.swapActiveSignals}
        memento.cyclePeriod=mc.cyclePeriod
        memento.L2CipherMapperStg={"wiring":mc.l2CipherMapper.wiring.extractAsMap()}
        return memento
    @classmethod
    def extractRotorSettingsFromRotorList(self,rotorList):
        result={}
        result["ORDER"]=[]
        result["OFFSET"]=[]
        for rotor in rotorList:
            result["ORDER"].append(rotor.id)
            result["OFFSET"].append(rotor.offset)
        return result

    @classmethod
    def applyMachineSettings(self,mc,settingsMemento):
        if not settingsMemento:
            raise Exception("Settings not found to ajdust !!")
        mc.rotorList=[]
        for r in settingsMemento.cipherRotorStg["ORDER"]:
            mc.rotorList.append(mc.rotorsStockMap[r])
        for i in range(len(settingsMemento.cipherRotorStg["OFFSET"])):
            mc.rotorList[i].offset=settingsMemento.cipherRotorStg["OFFSET"][i]

        mc.plugboard=PlugBoard(Wiring(settingsMemento.plugboardStg["wiring"]))

        mc.swapActiveSignals=settingsMemento.activeSwapSignals["SIGNALS"]
        mc.swapActiveSignalsCycleStep=settingsMemento.activeSwapSignals["CYCLE_STEP"]

        mc.swapRotorsLevel1=[]
        for r in settingsMemento.swappingL1Stg["ORDER"]:
            mc.swapRotorsLevel1.append(mc.l1SwappingRotorStockList[r])
        for i in range(len(settingsMemento.swappingL1Stg["OFFSET"])):
            mc.swapRotorsLevel1[i].offset=settingsMemento.swappingL1Stg["OFFSET"][i]

        mc.l1l2SeparatorSwitch.offset=settingsMemento.L1L2MapperStg["OFFSET"]

        mc.swapRotorsLevel2=[]
        for r in settingsMemento.swappingL2Stg["ORDER"]:
            mc.swapRotorsLevel2.append(mc.l2SwappingRotorStockList[r])
        for i in range(len(settingsMemento.swappingL2Stg["OFFSET"])):
            mc.swapRotorsLevel2[i].offset=settingsMemento.swappingL2Stg["OFFSET"][i]

        mc.l2CipherMapper=MapperSwitch(Wiring(settingsMemento.L2CipherMapperStg["wiring"]))

        mc.cyclePeriod=settingsMemento.cyclePeriod

        mc.settingsReady=True


    @classmethod
    def restoreMachinneSettings(cls,mc,memento):
        raise Exception("Unimplemented operation")
        pass
