from Switch import Switch
from CharIndexMap import CharIndexMap
from Wiring import Wiring
class PlugBoard(Switch):

    """
    String Format:

    X Y , M N

    example :
    00 01 , 03 04
    will create wiring of : 00->01 01->00 , 03->04 04->00
    """
    @classmethod
    def initFromString(cls,wiringStr):
        tuples=wiringStr.split(",")
        wiringMap={}
        for t in tuples:
            pair=t.split()
            fromPin=int(pair[0])
            toPin=int(pair[1])
            if fromPin in wiringMap or toPin in wiringMap:
                raise Exception("invalid duplicate plugbaord wiring")
            wiringMap[fromPin]=[toPin]
            wiringMap[toPin]=[fromPin]
        return PlugBoard(Wiring(wiringMap))

    def __init__(self,wiring):
        super().__init__(wiring)

    def signalIn(self,pin):
        if self.wiring.hasPairedPinFor(pin):
            return super().signalIn(pin)
        """ no wiring,just return the pin unchanged"""
        return pin
    def reverseSignal(self,pin):
        if self.wiring.hasPairedPinFor(pin):
            return super().signalIn(pin)
        """ no wiring,just return the pin unchanged"""
        return pin

    #return only different pairs e.g AX CD
    def getSettings(self):
        result=""
        coveredRange=[]
        for t in self.wiring.tupleList:
            if t[0] not in coveredRange and t[1] not in coveredRange:
                result+=str(t[0])+" "+str(t[1]) +","
                coveredRange.append(t[0])
                coveredRange.append(t[1])

        return result[0:len(result)-1] #no need for last ","
