from Plugboard import PlugBoard
from Rotor import Rotor
from Reflector import Reflector
from CharIndexMap import CharIndexMap
from Wiring import Wiring
import fixedSettings

class ModernEnigma:
    def __init__(self,rotorListDisplay,reflector,plugboard):
        #reverse to be easier to directly map visually by human
        self.rotorList=[]
        for r in reversed(rotorListDisplay):
            self.rotorList.append(r)
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
        for rotor in self.rotorList:
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

    def getWindowDisplay(self):
        result="Window||"
        for rotor in reversed(self.rotorList):
            result+=rotor.getDisplay()+" "
        return result
RI=fixedSettings.ROTORS["I"]
RII=fixedSettings.ROTORS["II"]
RIII=fixedSettings.ROTORS["III"]
REF_B=fixedSettings.REFLECTORS["B"]

r0=Rotor(Wiring(RI['wiring']),RI['stepping'])
r1=Rotor(Wiring(RII['wiring']),RII['stepping'])
r2=Rotor(Wiring(RIII['wiring']),RIII['stepping'])
reflector=Reflector(Wiring(REF_B))


plugboard=PlugBoard(Wiring())
mc=ModernEnigma([r0,r1,r2],reflector,plugboard)
MSG="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
for c in MSG:
    result=mc.processKeyPress(c)
    print(result)
    print(mc.getWindowDisplay())

# import pdb; pdb.set_trace()
