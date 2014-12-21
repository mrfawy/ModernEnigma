class MachineSettingsMemento(object):

    def __init__(self):
        self.cipherRotorStg={}
        self.plugboardStg={}
        self.activeSwapSignals=[]
        self.swappingL1Stg={}
        self.swappingL2Stg={}
        self.L1L2MapperStg={}
        self.L2CipherMapperStg={}
        self.cyclePeriod={}

    """
    Machine Settings Format:
    "(S) : space seprated
    (M): comma seprated
    (C): colon seprated
    selected cipher rotors init order(S)|Thier init offset(S)|plugboard(SC) pairs|active swap signals(S)|selected L1 rotors Order(S)|Thier init Offset(S)|L1 L2 Mapper offset|selected L2 rotors order(S)|Their init offset(S)|L2 Cipher Mapper wiring pairs (CSM)|(optional)Cycle period

    Example:
    01 03 05 | 00 15 18 |0 1 , 2 3 |11 19 30 |02 03 |22 25 |55 |07 03 | 11 13 |0: 01 03 ,04: 03 02 04|3

    Explaination:
    select rotors 01 ,03 ,05 to be ciphers in this order , set thier offset to 00, 15 ,18
    wire plugbaord as 0->1 1>0 , 2->3 , 3>2
    set swapping active signals to 11 , 19 and 30
    select L1 rotors 02 ,03 in this order , and set thier offset to 22 and 25

    set L1 L2 mapper offset to 55

    select L2 rotors 07 and 03 in this order and set thier offst to 11 and 13

    create a new L2 to Cipher mapper with size 3 (# of selcted cipher rotors),
    and set its wiring 0->01 0->03 , 04->03 04->02 04->04

    """
    @classmethod
    def InitInstanceFromStrStg(cls,settingStr):
        if not MachineSettingsMemento.validateSettingString(settingStr):
            raise Exception("Invalid machine settings \n"+settingStr)

        result=MachineSettingsMemento()
        settingsParts=settingStr.split('|')

        cipherRotorOrderStg=settingsParts[0]
        cipherRotorOffsetStg=settingsParts[1]
        result.cipherRotorStg=MachineSettingsMemento.parseRotorStg(cipherRotorOrderStg,cipherRotorOffsetStg)

        plugboardWiringStg=settingsParts[2]
        result.plugboardStg["wiring"]=plugboardWiringStg

        activeSwapStg=settingsParts[3]
        for c in activeSwapStg.split(" "):
            if len(c)>0:
                result.activeSwapSignals.append(int(c))

        L1RotorOrderStg=settingsParts[4]
        L1RotorOffsetStg=settingsParts[5]

        result.swappingL1Stg=MachineSettingsMemento.parseRotorStg(L1RotorOrderStg,L1RotorOffsetStg)

        L1L2MapperOffset=settingsParts[6]
        result.L1L2MapperStg["OFFSET"]=L1L2MapperOffset

        L2RotorOrderStg=settingsParts[7]
        L2RotorOffsetStg=settingsParts[8]
        result.swappingL2Stg=MachineSettingsMemento.parseRotorStg(L2RotorOrderStg,L2RotorOffsetStg)

        L2CipherWiringStg=settingsParts[9]
        result.L2CipherMapperStg=MachineSettingsMemento.parseMapperStg(L2CipherWiringStg)

        if len(settingsParts)>10:
            result.cyclePeriod=int(settingsParts[10])

        return result

    @classmethod
    def parseMapperStg(cls,strStg):
        result={"wiring":{}}
        tupleList=strStg.split(",")
        for t in tupleList:
            mapping=t.split(":")
            fromPin=int(mapping[0])
            toPins=mapping[1].split(" ")
            result["wiring"][fromPin]=[]
            for toPin in toPins:
                if len(toPin) >0:
                    result["wiring"][fromPin].append(int(toPin))

        return result

    @classmethod
    def parseRotorStg(cls,orderStg,offsetStg):
        result={}
        result["ORDER"]=[]
        for c in orderStg.split():
            result["ORDER"].append(int(c))

        result["OFFSET"]=[]
        for c in offsetStg.split():
            result["OFFSET"].append(int(c))

        return result



    @classmethod
    def validateSettingString(cls,strStg):
        if len(strStg.split("|"))<10:
            return False
        return True

    @classmethod
    def applyMachineSettings(self,mc,settingsMemento):
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


    def createActiveSwapSignalsConfig(self,id="ACTV",count=None):
        if not count:
            count=self.random.nextInt(self.SWAP_ACTIVE_SIGNALS_COUNT_MIN,self.SWAP_ROTOR_L1_COUNT_MAX)
        activeSwapCfg={}
        activeSwapCfg["ID"]=id
        activeSwapCfg["SIGNALS"]=self.getShuffledSequence()[0:count]

        return activeSwapCfg
    def print(self):
        print(self.cipherRotorStg)
        print(self.plugboardStg)
        print(self.activeSwapSignals)
        print(self.swappingL1Stg)
        print(self.swappingL2Stg)
        print(self.L1L2MapperStg)
        print(self.L2CipherMapperStg)
        print(self.cyclePeriod)

