from CharIndexMap import CharIndexMap

class Wiring(object):
    def __init__(self,config=None):
        self.tupleList=[]
        if config:
            self.connectByConfig(config)
        else:
            self.loadDefaultWiring()

    def loadDefaultWiring(self):
        self.size=CharIndexMap.getRangeSize()
        for i in range(CharIndexMap.getRangeSize()):
            self.addConnection(i,i)

    def addConnection(self,x,y):
        self.tupleList.append((x,y))

    def hasPairedPinFor(self,pin):
        for entry in self.tupleList:
            if pin ==entry[0]:
                return True
        return False


    def getMultiPairdPin(self,pin):
        result=[]
        for entry in self.tupleList:
            if pin==entry[0]:
                result.append(entry[1])
        if len(result)==0:
            raise("Multi Paired Pin not found")
        return result
    def getPairedPin(self,pin):
        for entry in self.tupleList:
            if pin ==entry[0]:
                return entry[1]
        raise("Paired Pin Not Found")
        return None

    def getPairedPinRev(self,pin):
        for entry in self.tupleList:
            if pin ==entry[1]:
                return entry[0]
        raise("Paired Pin Not Found")
        return None

    def connectByConfig(self,config):
        self.inputSize=len(config)
        for key,value in config.items():
            fromPin=int(key)
            for toPin in value:
                self.addConnection(fromPin,toPin)

    def printWiring(self):
        for entry in self.tupleList:
            print(str(entry))
