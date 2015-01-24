from ModernEnigma import ModernEnigma
from RandomGenerator import RandomGenerator
from MachineSettingsMemento import MachineSettingsMemento

class Level(object):
    def __init__(self,baseMachineStg,levelMachineStg,seed=None):
        self.baseStg=baseMachineStg
        self.levelStg=levelMachineStg
        self.random=RandomGenerator(seed)
        self.inputMsg=""
        self.outputMsg=""
        self.i={0:[],1:[]}
        self.j={0:[],1:[]}
        self.k={0:[],1:[]}
        self.l={0:[],1:[]}
        self.s={0:[],1:[]}
        self.st={0:[],1:[]}
        self.xor={0:[],1:[]}
        self.baseMcBlkSize={}
        self.levelMcBlkSize={}
        self.initLevelValues()

    def initLevelValues(self,min=1,max=2,minBlkSize=2,maxBlkSize=64):
        self.i[0]=self.random.nextInt(min,max)
        self.i[1]=self.random.nextInt(min,max)
        self.j[0]=self.random.nextInt(min,max)
        self.j[1]=self.random.nextInt(min,max)
        self.k[0]=self.random.nextInt(min,max)
        self.k[1]=self.random.nextInt(min,max)
        self.l[0]=self.random.nextInt(min,max)
        self.l[1]=self.random.nextInt(min,max)
        self.s[0]=self.random.nextInt(min,max)
        self.s[1]=self.random.nextInt(min,max)
        self.st[0]=self.random.nextInt(min,max)
        self.st[1]=self.random.nextInt(min,max)
        self.xor[0]=self.random.nextInt()
        self.xor[1]=self.random.nextInt()
        self.baseMcBlkSize[0]=self.random.nextInt(minBlkSize,maxBlkSize)
        self.baseMcBlkSize[1]=self.random.nextInt(minBlkSize,maxBlkSize)
        self.levelMcBlkSize[0]=self.random.nextInt(minBlkSize,maxBlkSize)
        self.levelMcBlkSize[1]=self.random.nextInt(minBlkSize,maxBlkSize)

    def getAsMap(self):
        result={}
        result["baseStg"]=self.baseStg.getAsMap()
        result["levelStg"]=self.levelStg.getAsMap()
        result["inputMsg"]=self.inputMsg
        result["outputMsg"]=self.outputMsg
        result["i"]=self.i
        result["j"]=self.j
        result["k"]=self.k
        result["l"]=self.l
        result["s"]=self.s
        result["st"]=self.st
        result["xor"]=self.xor
        result["baseMcBlkSize"]=self.baseMcBlkSize
        result["levelMcBlkSizse"]=self.levelMcBlkSize
        return result
    @classmethod
    def loadFromMap(cls,inputMap):
        level=Level(None,None)
        level.baseStg=MachineSettingsMemento.loadFromMap(inputMap["baseStg"])
        level.levelStg=MachineSettingsMemento.loadFromMap(inputMap["levelStg"])
        level.inputMsg=inputMap["inputMsg"]
        level.outputMsg=inputMap["outputMsg"]
        level.i=inputMap["i"]
        level.j=inputMap["j"]
        level.k=inputMap["k"]
        level.l=inputMap["l"]
        level.s=inputMap["s"]
        level.st=inputMap["st"]
        level.xor=inputMap["xor"]
        level.baseMcBlkSize=inputMap["baseMcBlkSize"]
        level.levelMcBlkSize=inputMap["levelMcBlkSizse"]
        return level
