from CharIndexMap import CharIndexMap
from Wiring import Wiring
class Switch(object):
    def __init__(self,wiring):
        self.wiring=wiring
    def signalIn(self,indexIn):
        return self.wiring.getPairedPin(indexIn)

    def reverseSignal(self,indexReverseIn):
        return self.wiring.getPairedPinRev(indexReverseIn)

conf="EKMFLGDQVZNTOWYHXUSPAIBRCJ"
w=Wiring(conf)
# s=Switch()
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
