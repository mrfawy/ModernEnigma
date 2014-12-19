from CharIndexMap import CharIndexMap

class Wiring(object):
    def __init__(self,config=None):
        self.tupleList=[]
        if config:
            self.connectByConfig(config)
        else:
            self.loadDefaultWiring()

    def initWiringFromTupleList(self,tupleList):
        self.tupleList=[]
        for t in tupleList:
            self.addConnection(t[0],t[1])

    def loadDefaultWiring(self):
        for i in range(CharIndexMap.getRangeSize()):
            self.addConnection(i,i)

    def addConnection(self,x,y):
        self.tupleList.append((x,y))

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
        for i in range(len(config)):
            self.addConnection(i,CharIndexMap.charToIndex(config[i]))

    def printWiring(self):
        for entry in self.tupleList:
            print(str(entry))
