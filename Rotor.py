from CharIndexMap import CharIndexMap
from Switch import Switch
class Rotor(Switch):
    def __init__(self,offset=0,notchIndexList=[]):
        super().__init__()
        self.offset=offset
        self.size=CharIndexMap.getRangeSize()
        self.notchIndexList=notchIndexList

    def signalIn(self,indexIn):
        newIndexIn=(self.offset+indexIn)%self.size
        output= super().signalIn(newIndexIn)
        return (output-self.offset)%self.size

    def reverseSignal(self,indexReverseIn):
        newReverseIndexIn=(self.offset+indexReverseIn)%self.size
        output= super().reverseSignal(newReverseIndexIn)
        return (output-self.offset)%self.size

    def adjustDisplay(self,char):
        self.offset=CharIndexMap.charIndex(char)

    def getDisplay(self):
        return CharIndexMap.indexToChar(self.offset)

    #return True if notch touches to mark rotate next Rotor
    def rotate(self):
        self.offset=(self.offset+1)%self.size
        if(self.offset in self.notchIndexList):
            return True
        return False

# #test
#import pdb; pdb.set_trace()
# r=Rotor()
# config="EKMFLGDQVZNTOWYHXUSPAIBRCJ"
# r.connectByConfig(config)
# r.printConnections()
# for i in range(0,5):
#     print(CharIndexMap.indexToChar(r.signalIn(0)))
#     r.rotate()
#
