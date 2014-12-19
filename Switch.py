from CharIndexMap import CharIndexMap
from Wiring import Wiring
class Switch(object):
    def __init__(self,wiring):
        self.wiring=wiring
    def signalIn(self,indexIn):
        return self.wiring.getPairedPin(indexIn)

    def reverseSignal(self,indexReverseIn):
        return self.wiring.getPairedPinRev(indexReverseIn)

