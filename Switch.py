from CharIndexMap import CharIndexMap
class Switch(object):
    def __init__(self,charIndexMap):
        self.charIndexMap=charIndexMap
        self.inputWiring=[]
        self.outputWiring=[]

        # default connection , no change x <-->x
        for i in range(charIndexMap.getRangeSize()):
            self.inputWiring.append(i)
            self.outputWiring.append(i)

    def connectByChar(self,xChar,yChar):
        xIndex=self.charIndexMap.charToIndex(xChar)
        yIndex=self.charIndexMap.charToIndex(yChar)
        return self.connectByIndex(xIndex,yIndex)

    # there is a constrain here , select from input , select from output iff not busy, not all permutations possible
    def connectByIndex(self,xIndex,yIndex):
        #save old connections
        xcharDualIndex=self.inputWiring[xIndex]
        ycharDualIndex=self.outputWiring[yIndex]
        #now reset connections
        # self.outputWiring[xcharDualIndex]=xcharDualIndex
        # self.inputWiring[ycharDualIndex]=ycharDualIndex

        #add new connection
        self.inputWiring[xIndex]=yIndex
        self.outputWiring[yIndex]=xIndex

    def printConnections(self):
        for i in range(len(self.inputWiring)):
            print (self.charIndexMap.indexToChar(i)+":-->"+self.charIndexMap.indexToChar(self.inputWiring[i]) +"||"+self.charIndexMap.indexToChar(i)+"<--"+self.charIndexMap.indexToChar(self.outputWiring[i]))
    def signalIn(self,indexIn):
        return self.inputWiring[indexIn]

    def reverseSignal(self,indexReverseIn):
        return self.outputWiring[indexReverseIn]
#
# m=CharIndexMap()
# s=Switch(m)
# s.printConnections()
# print ("============AX  BZ =========================")
# s.connectByChar("A","X")
# s.connectByChar("B","Z")
# s.printConnections()
#
# print ("============XA ZB ======================")
# import pdb; pdb.set_trace()
# s.connectByChar("X","A")
# s.connectByChar("Z","B")
# s.printConnections()
