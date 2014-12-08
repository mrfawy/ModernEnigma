from CharIndexMap import CharIndexMap

class Wiring(object):
    def __init__(self,config=None):
        self.tupleList=[]
        if config:
            self.connectByConfig(config)
        else:
            self.loadDefaultWiring()
    def loadDefaultWiring(self):
        for i in range(CharIndexMap.getRangeSize()):
            self.addConnection(i,i)

    def addConnection(self,x,y):
        self.tupleList.append((x,y))

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
