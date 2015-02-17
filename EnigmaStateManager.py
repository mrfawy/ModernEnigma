import threading
import time
from queue import Queue
class EnigmaStateManager:

    def __init__(self,num_worker_threads=4):
        self.machineStateTable={}
        self.workRequestMap={}
        self.workQueue=Queue()
        self.num_worker_threads=num_worker_threads
        self.finished=False
        self.run()

    def processWorkQueue(self):
        while not self.finished:
            workRequest=self.workQueue.get()
            self.generateState(workRequest)
            self.workQueue.task_done()
            time.sleep(0.2)

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
            t.daemon =True
            t.start()

    def retreiveMachineState(self,machineId,stateNumber):

        if machineId in self.machineStateTable and stateNumber in self.machineStateTable[machineId]:
            return self.machineStateTable[machineId][stateNumber]
        else:
            """request already in queue , need to wait till it's ready"""
            if machineId in self.workRequestMap and  stateNumber <= self.workRequestMap[machineId]:
                while (machineId not in self.machineStateTable) or (stateNumber not in self.machineStateTable[machineId]):
                    time.sleep(0.1)

                return self.machineStateTable[machineId][stateNumber]
            else:
                raise ("No workRequest in workQueue for this machine state !!")


    def generateMachineState(self,machineId,machine,generatedStepsCount):
        request={}
        request["MCID"]=machineId
        request["STCount"]=generatedStepsCount
        request["MC"]=machine
        self.workQueue.put(request)
        if machineId in self.workRequestMap:
            lastStep=self.workRequestMap[machineId]
            lastStep+=generatedStepsCount
            self.workRequestMap[machineId]=lastStep
        else:
            self.workRequestMap[machineId]=generatedStepsCount

    def addMachineStateToTable(self,machineId,stateNumber,state):
        if machineId not in self.machineStateTable:
            self.machineStateTable[machineId]={}

        entry=self.machineStateTable[machineId]
        entry[stateNumber]=state


