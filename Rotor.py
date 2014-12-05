from CharIndexMap import CharIndexMap
from Switch import Switch
class Rotor(Switch):
    def __init__(self,charIndexMap,offset=0,notchIndexList=[]):
        super().__init__(charIndexMap)
        self.offset=offset
        self.size=charIndexMap.getRangeSize()
        self.notchIndexList=notchIndexList

    def signalIn(self,indexIn):
        newIndexIn=(self.offset+indexIn)%self.size
        import pdb; pdb.set_trace()
        output= super().signalIn(newIndexIn)
        return (output-self.offset)%self.size
    def reverseSignal(self,indexReverseIn):
        newReverseIndexIn=(offset+indexReverseIn)%self.size
        output= super().reverseSignal(newReverseIndexIn)
        return (output-offset)%self.size

    def adjustDisplay(self,char):
        self.offset=self.charIndexMap.charIndex(char)
    def getDisplay(self):
        return self.charIndexMap.indexToChar(self.offset)
    #return True if notch touches to mark rotate next Rotor
    def rotate(self):
        self.offset=(self.offset+1)%self.size
        if(self.offset in self.notchIndexList):
            return True
        return False

#test
m=CharIndexMap()
r=Rotor(m)
for i in range(0,2*r.size):
    print(r.signalIn(0))
    r.rotate()

