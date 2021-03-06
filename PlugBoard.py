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

    def signalIn(self,pins):
        result=[]
        for pin in pins:
            if self.wiring.hasPairedPinFor(pin):
                result.append(super().signalIn([pin])[0])
            else:
                result.append(pin)
        return result
    def reverseSignal(self,pins):
        result=[]
        for pin in pins:
            if self.wiring.hasPairedPinFor(pin):
                result.append(super().signalIn([pin])[0])
            else:
                result.append(pin)
        return result

    #return only different pairs e.g AX CD
    def getSettings(self):
        result=""
        coveredRange=[]
        for key,value in self.wiring.getAsMap().items():
            fromPin=key
            toPin=value[0]
            if fromPin not in coveredRange and toPin not in coveredRange:
                result+=str(fromPin)+" "+str(toPin) +","
                coveredRange.append(fromPin)
                coveredRange.append(toPin)

        return result[0:len(result)-1] #no need for last ","
