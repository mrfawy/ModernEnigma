class MachineSettingsMemento(object):

    def __init__(self):
        self.cipherRotorStg={}
        self.plugboardStg={}
        self.activeSwapSignals=[]
        self.swappingRotorStg={}

    def getAsMap(self):
        result={}
        result["cipherRotorStg"]=self.cipherRotorStg
        result["plugboardStg"]=self.plugboardStg
        result["activeSwapSignals"]=self.activeSwapSignals
        result["swappingRotorStg"]=self.swappingRotorStg
        return result

    @classmethod
    def loadFromMap(cls,inputMap):
        memento=MachineSettingsMemento()
        memento.cipherRotorStg=inputMap["cipherRotorStg"]
        memento.plugboardStg=inputMap["plugboardStg"]
        memento.activeSwapSignals=inputMap["activeSwapSignals"]
        memento.swappingRotorStg=inputMap["swappingRotorStg"]
        return memento



