from CharIndexMap import CharIndexMap
from Wiring import Wiring
class Switch(object):
    def __init__(self,wiring):
        self.wiring=wiring
    def signalIn(self,indexInList):
        result =[]
        for pin in indexInList:
            result.append(self.wiring.getPairedPin(pin))
        return result

    def reverseSignal(self,indexReverseInList):
        result=[]
        for pin in indexReverseInList:
            result.append(self.wiring.getPairedPinRev(pin))
        return result

