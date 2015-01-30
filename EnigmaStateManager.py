import threading
import time
from queue import Queue
class EnigmaStateManager:

    def __init__(self,num_worker_threads=5):
        self.machineStateTable={}
        self.workQueue=Queue()
        self.num_worker_threads=num_worker_threads
        self.finished=False
        self.run()

    def processWorkQueue(self):
        print("checking queue ")
        while not self.finished:
            workRequest=self.workQueue.get()
            self.generateState(workRequest)
            self.workQueue.task_done()
            time.sleep(0.5)

    def generateState(self,workRequest):
        mc=workRequest["MC"]
        mcId=workRequest["MCID"]
        inputBlk=range(mc.getCipherRotorsSize())
        print("processing work request")
        for i in range(workRequest["STCount"]):
            outputBlk=mc.processKeyListPress(inputBlk)
            stateMap=self.createStateMap(inputBlk,outputBlk)
            self.addMachineStateToTable(mcId,i,stateMap)

    def createStateMap(self,inputSeq,outputSeq):
        result={}
        for i in range(len(inputSeq)):
            result[i]=outputSeq[i]
        return result

    def run(self):
        for i in range(self.num_worker_threads):
            t = threading.Thread(target=self.processWorkQueue)
            # t.daemon = True
            t.start()

    def retreiveMachineState(self,machineId,stateNumber):
        entryID=self.getEntryId(machineId,stateNumber)
        if entryID in self.machineStateTable:
            return self.machineStateTable[entryID]
        else:
            self.generateMachineState(machineId,stateNumber)
            return self.machineStateTable[entryID]

    def generateMachineState(self,machineId,machine,generatedStepsCount):
        request={}
        request["MCID"]=machineId
        request["STCount"]=generatedStepsCount
        request["MC"]=machine
        self.workQueue.put(request)

    def addMachineStateToTable(self,machineID,stateNumber,state):
        key=machineID+"|"+str(stateNumber)
        self.machineStateTable[key]=state
        print(key)

    def getEntryId(self,machineId,stateNumber):
        return str(machineId)+"|"+str(stateNumber)

