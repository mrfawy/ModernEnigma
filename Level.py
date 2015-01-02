from ModernEnigma import ModernEnigma
from RandomGenerator import RandomGenerator

class Level(object):
    def __init__(self,baseMachineStg,levelMachineStg,random=RandomGenerator()):
        self.baseStg=baseMachineStg
        self.levelStg=levelMachineStg
        self.random=random
        self.inputMsg=""
        self.outputMsg=""
        self.i={0:[],1:[]}
        self.j={0:[],1:[]}
        self.k={0:[],1:[]}
        self.l={0:[],1:[]}
        self.s={0:[],1:[]}
        self.st={0:[],1:[]}
        self.baseMcBlkSize={}
        self.levelMcBlkSize={}
        self.initLevelValues()

    def initLevelValues(self,min=3,max=9,minBlkSize=4,maxBlkSize=8):
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
        result["baseMcBlkSize"]=self.baseMcBlkSize
        result["levelMcBlkSizse"]=self.levelMcBlkSize
        return result
