from Switch import Switch
from CharIndexMap import CharIndexMap
from Wiring import Wiring
class PlugBoard(Switch):
    def __init__(self,wiring):
        if isinstance(wiring,str):
            #load wiring from string
            #pairs are 2 char , space separated e.g AX BY CZ
            pairs=wiring.split()
            wireRange=[]
            for c in CharIndexMap.getRange():
                wireRange.append(c)
            for pair in pairs:
                xchar=pair[0]
                ychar=pair[1]
                wireRange[CharIndexMap.charToIndex(xchar)]=ychar
                wireRange[CharIndexMap.charToIndex(ychar)]=xchar
            mappingStr=""
            for c in wireRange:
                mappingStr+=c
            super().__init__(Wiring(mappingStr))
        else:
            super().__init__(wiring)

    #return only different pairs e.g AX CD
    def getSettings(self):
        result=""
        coveredRange=[]
        for pin in range(CharIndexMap.getRangeSize()):
            if pin in coveredRange:
                continue
            pout=self.signalIn(pin)
            if pin !=pout :
                inputChar=CharIndexMap.indexToChar(pin)
                outputChar=CharIndexMap.indexToChar(pout)
                result+=inputChar+outputChar
                coveredRange.append(pin)
                coveredRange.append(pout)
        return result
