from EnigmaMapProducer import EnigmaMapProducer
from ModernEnigma import ModernEnigma
from queues import Queue

"""
Encrypts/decrypts a message

input a list of machines ( shadows) - ordered , seed to generate the reflector

it creates queues and start machine producers , for each input byte it collect maps from queues and enc/decrypt

"""
class ShadowEncryptor:
    def __init__(self,machineShadowList):
        self.machineShadowList=machineShadowList
        self.initProducers()
        self.initReflector()

    def initProducers(self):
        size=self.machineShadowList.len
        self.queues=[]
        self.producers=[]
        for i in range(size):
            q=Queue()
            producer=EnigmaMapProducer(q,self.machineShadowList[i])
            self.producers.append(producer)
            self.queues.append(q)
            producer.start()
    def initReflector(self):
        self.reflector=None


    def processStream(self,stream):
        output=[]
        for b in stream:
            substituonMapList=[]
            i=b
            for q in self.queues:
                substituonMapList.append(q.get(True))
            for substituonMap in substituonMapList:
                y=substutionMap[i]
            #y=self.reflector.signalIn([y]
            for substituonMap in reversed(substituonMapList):
                y=substituonMap[y]
            output.append[y]
        for producer in self.producers:
            producer.stop()





