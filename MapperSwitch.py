from Wiring import Wiring
from Rotor import Rotor

"""Extends Switch , allowing for single Pin in , and multi-Pin out"""
class MapperSwitch(Rotor):
    def __init__(self,wiring):
        super().__init__(0,wiring)
    def signalIn(self,indexIn):
        newIndexIn=(self.offset+indexIn)%self.size
        mutliOutput=self.wiring.getMultiPairdPin(indexIn)
        for i in range(len(mutliOutput)):
            mutliOutput[i]=(mutliOutput[i]-self.offset)%self.size
        return mutliOutput

    def reverseSignal(self,indexReverseIn):
        raise Exception("Unsupported operation by SwappingSwitch")

