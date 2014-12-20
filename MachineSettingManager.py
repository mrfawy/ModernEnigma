from MachineSettingsMemento import MachineSettingsMemento
from RandomGenerator import RandomGenerator

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
        memento.swappingL2Stg=self.generateDefaultSettingsForRotorStock(mc.l1SwappingRotorStockList)

        memento.L1L2MapperStg["OFFSET"]=0

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
        memento=MachineSettingsMemento()
        raise Exception("Unimplemented operation")
        return memento
    @classmethod
    def applyMachineSettings(self,mc,settingsMemento):
        if not settingsMemento:
            raise Exception("Settings not found to ajdust !!")
        mc.rotorList=[]
        for r in settingsMemento.cipherRotorStg["ORDER"]:
            mc.rotorList.append(mc.rotorsStockMap[r])
        for i in len(settingsMemento.cipherRotorStg["OFFSET"]):
            mc.rotorList[i].offset=settingsMemento.cipherRotorStg["OFFSET"][i]

        mc.plugboard=PlugBoard(Wiring(settingsMemento.plugboardStg["wiring"]))

        mc.applyActivePins=settingsMemento.activePins

        for r in settingsMemento.swappingL1Stg["ORDER"]:
            mc.swapRotorsLevel1.append(mc.l1SwappingRotorStockList[r])
        for i in len(settingsMemento.swappingL1Stg["OFFSET"]):
            mc.swapRotorsLevel1[i].offset=settingsMemento.swappingL1Stg["OFFSET"][i]

        mc.l1l2SeparatorSwitch.offset=settingsMemento.L1L2MapperStg["OFFSET"]

        for r in settingsMemento.swappingL2Stg["ORDER"]:
            mc.swapRotorsLevel2.append(mc.l2SwappingRotorStockList[r])
        for i in len(settingsMemento.swappingL2Stg["OFFSET"]):
            mc.swapRotorsLevel2[i].offset=settingsMemento.swappingL2Stg["OFFSET"][i]

        mc.l2CipherMapper=MapperSwitch(Wiring(settingsMemento.l2CipherMapper["wiring"]))

        mc.cyclePeriod=settingsMemento.cyclePeriod

        mc.settingsReady=True


    @classmethod
    def restoreMachinneSettings(cls,mc,memento):
        raise Exception("Unimplemented operation")
        pass
