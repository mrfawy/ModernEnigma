from Wiring import Wiring
from Switch import Switch

"""Extends Switch , allowing for single Pin in , and multi-Pin out"""
class MapperSwitch(Switch):
    def __init__(self,wiring):
        super().__init__(wiring)
    def signalIn(self,indexIn):
        return self.wiring.getMultiPairdPin(indexIn)

    def reverseSignal(self,indexReverseIn):
        raise Exception("Unsupported operation by SwappingSwitch")

