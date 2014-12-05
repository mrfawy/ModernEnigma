from Plugboard import PlugBoard
from Rotor import Rotor
from Reflector import Reflector
from CharIndexMap import CharIndexMap
from Wiring import Wiring

class ModernEnigma:
    def __init__(self,rotorList,reflector,plugboard):
        self.rotorList=rotorList
        self.reflector=reflector
        self.plugboard=plugboard

    def processKeyPress(self,char):
        indexIn=CharIndexMap.charToIndex(char)
        # print("indexIn"+str(indexIn))
        lastOut=self.plugboard.signalIn(indexIn)
        # print("plug"+str(lastOut))
        for rotor in self.rotorList:
            lastOut=rotor.signalIn(lastOut)
            # print("rotorIn"+str(lastOut))
        lastReverseIn=self.reflector.signalIn(lastOut)
        # print("reflectorRev"+str(lastReverseIn))
        for rotor in reversed(self.rotorList):
            lastReverseIn=rotor.reverseSignal(lastReverseIn)
            # print("rotorReve"+str(lastReverseIn))
        output=self.plugboard.reverseSignal(lastReverseIn)
        # print("plugRev"+str(output))

        notchFlag=False
        for i  in range(len(self.rotorList)) :
            rotor=self.rotorList[i]
            if i==0:
                notchFlag=rotor.rotate()
                continue
            if notchFlag:
                notchFlag=rotor.rotate()
        return CharIndexMap.indexToChar(output)

rotor1Wiring=Wiring("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
rotor1=Rotor(rotor1Wiring,[1,3])
rotor2Wiring=Wiring("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
rotor2=Rotor(rotor1Wiring,[1,3])
w=Wiring()
reflectorWiring=Wiring("YRUHQSLDPXNGOKMIEBFZCWVJAT")
reflector=Reflector(reflectorWiring)
plugboard=PlugBoard(w)
mc=ModernEnigma([rotor1,rotor2],reflector,plugboard)
MSG="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
for c in MSG:
    print("R0:"+mc.rotorList[0].getDisplay())
    print("R1:"+mc.rotorList[1].getDisplay())
    result=mc.processKeyPress(c)
    print(result)

# import pdb; pdb.set_trace()
