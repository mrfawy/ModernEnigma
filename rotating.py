from Rotor import Rotor

class RotorSwapper(object):
    def __init__(self,machine):
        self.machine=machine
        self.swapRotorsLevel1=self.machine.swapRotorsLevel1
        self.swapRotorsLevel2=self.machine.swapRotorsLevel2
        self.swapSeparatorSwitch=self.machine.swapSeparatorSwitch
        self.baseSwapActiveChars=self.machine.baseSwapActiveChars
        self.rotorList=self.machine.rotorList

    def processSignalSwapping(self,char):
        indexIn=CharIndexMap.charToIndex(char)
        # lastOut=self.plugboard.signalIn(indexIn)
        lastout=(indexIn)
        activePins=[]
        for c in self.baseSwapActiveChars:
            activePins.append(CharIndexMap.charToIndex(c))
        if lastout not in activePins:
            activePins.append(lastout)

        swapLevel1Result=self.applyActivePins(self.swapRotorsLevel1,activePins)
        swapLevel2Input=self.applyActivePins([self.swapSeparatorSwitch],swapLevel1Result)
        swapLevel2Result=self.applyActivePins(self.swapRotorsLevel2,swapLevel2Input)

        self.swapRotors(self.rotorList,swapLevel2Result)

        self.processStepping(self.swapRotorsLevel1)
        self.processStepping(self.swapRotorsLevel2)



    def applyActivePins(self,rotors,pins):
        resultPins=[]
        for pin in pins:
            lastout=pin
            for rotor in rotors:
                print("offset"+str(rotor.offset))
                lastout=rotor.signalIn(lastout)
            if lastout not in resultPins:
                resultPins.append(lastout)
        return resultPins
    def processStepping(self,rotors):
        notchFlag=False
        for i  in range(len(rotors)) :
            rotor=rotors[i]
            if i==0:
                notchFlag=rotor.rotate()
                continue
            if notchFlag:
                notchFlag=rotor.rotate()

    def swap(self,rotorList,i,j):
        print("swapping:"+str(i)+str(j))
        tmp=rotorList[i]
        rotorList[i]=rotorList[j]
        rotorList[j]=tmp

    def swapRotors(self,rotorList,swapIndexList):
        for index in swapIndexList:
            self.swap(rotorList,index,(index+1)%len(rotorList))



class tmptype(object):
    def __init__(self):
        self.swapRotorsLevel1=[]
        self.swapRotorsLevel2=[]
        self.swapSeparatorSwitch=None
        self.baseSwapActiveChars=None
        self.rotorList=None

from Wiring import Wiring
from CharIndexMap import CharIndexMap
mc=tmptype()
mc.swapRotorsLevel1=[]
l1r1=Rotor("l1r1",Wiring("FEDCBA"))
mc.swapRotorsLevel1.append(l1r1)

mc.swapSeparatorSwitch=Rotor("sep",Wiring("AABCCC"))
mc.rotorList=[Rotor("A",Wiring()),Rotor("B",Wiring()),Rotor("C",Wiring())]
mc.baseSwapActiveChars=["F"]

swapper=RotorSwapper(mc)

test="FFFFFF"
for t in test:
    print ("============")
    swapper.processSignalSwapping(t)
    for r in mc.rotorList:
        print (r.id)

# swapper level 1 :
#     rotor size = 64
#     input will  be k( fixed indexes as per settings  +current char )
#     output will be max K active pins in range 64
#     in last rotor output map it to pins of level 2
#         for each pin in L1 , pick random pins in L2 , map those pins
#             this makes sure all inputs are mapped
#
# swapper level 2
#     rotor size=N ( number of rotor List)
#     input will be max  K active in range N
#       output , e.g 0,1,2 -> swap cipher rotor 0 , 1 ,2
# swap rule : if rotor=x > swap with x+1
# if rotor =N , swap , with 0

