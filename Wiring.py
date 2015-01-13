from CharIndexMap import CharIndexMap

class Wiring(object):
    def __init__(self,config=None):
        self.signalInMap={}
        self.signalReversedMap={}
        if config:
            self.connectByConfig(config)
        else:
            self.loadDefaultWiring()

    def loadDefaultWiring(self):
        self.inputSize=CharIndexMap.getRangeSize()
        for i in range(CharIndexMap.getRangeSize()):
            self.addConnection(i,i)

    def addConnection(self,x,y):
        if x not in self.signalInMap:
            self.signalInMap[x]=[]
        self.signalInMap[x].append(y)
        if y not in self.signalReversedMap:
            self.signalReversedMap[y]=[]
        self.signalReversedMap[y].append(x)

    def hasPairedPinFor(self,pin):
        if pin in self.signalInMap:
            return True
        return False


    def getMultiPairdPin(self,pin):
        result=self.signalInMap[pin]
        if not result:
            raise("Multi Paired Pin not found")
        return result
    def getPairedPin(self,pin):
        result=self.signalInMap[pin]
        if not result:
            raise("Paired Pin Not Found")
        return result[0]

    def getPairedPinRev(self,pin):
        result=self.signalReversedMap[pin]
        if not result:
            raise("Paired Pin Not Found")
        return result[0]

    def connectByConfig(self,config):
        items=config.items()
        self.inputSize=len(items)
        for key,value in items:
            fromPin=int(key)
            for toPin in value:
                self.addConnection(fromPin,toPin)

    def getAsMap(self):
        return self.signalInMap

