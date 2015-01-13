from CharIndexMap import CharIndexMap
from Switch import Switch
from Wiring import Wiring
class Rotor(Switch):
    def __init__(self,id,wiring,notchSeq=[],offset=0):
        super().__init__(wiring)
        self.id=id
        self.offset=offset
        self.size=wiring.inputSize
        self.notchIndexList=[]
        for n in notchSeq:
            self.notchIndexList.append(n)

    def signalIn(self,indexInList):
        newIndexIn=[(self.offset+x)%self.size for x in indexInList]
        output= super().signalIn(newIndexIn)
        return [(x-self.offset)%self.size for x in output]

    def reverseSignal(self,indexReverseInList):
        newReverseIndexIn=[(self.offset+x)%self.size for x in indexReverseInList]
        output= super().reverseSignal(newReverseIndexIn)
        return [(x-self.offset)%self.size for x in output]

    def adjustDisplay(self,offset):
        self.offset=offset

    def getDisplay(self):
        return self.offset

    #return True if notch touches to mark rotate next Rotor
    def rotate(self):
        flipNextRotorFlag=False
        self.offset=(self.offset+1)%self.size
        if(self.offset in self.notchIndexList):
            flipNextRotorFlag=True
        return flipNextRotorFlag

# #test
#import pdb; pdb.set_trace()
