from Switch import Switch
from CharIndexMap import CharIndexMap
class PlugBoard(Switch):
    def __init__(self):
        super().__init__()

    #override connection
    def connectByIndex(self,xIndex,yIndex):
        #remove old connections
        xcharDualIndex=self.inputWiring[xIndex]
        ycharDualIndex=self.outputWiring[yIndex]
        #now reset connections
        # self.inputWiring[xIndex]=xIndex
        self.inputWiring[xcharDualIndex]=xcharDualIndex
        self.outputWiring[xcharDualIndex]=xcharDualIndex

        # self.inputWiring[yIndex]=yIndex
        self.inputWiring[ycharDualIndex]=ycharDualIndex
        self.outputWiring[ycharDualIndex]=ycharDualIndex

        #add new connection
        self.inputWiring[xIndex]=yIndex
        self.outputWiring[yIndex]=xIndex

# p=PlugBoard()
# p.connectByChar("A","C")
# p.connectByChar("B","A")
# p.connectByChar("C","B")
# p.printConnections()
