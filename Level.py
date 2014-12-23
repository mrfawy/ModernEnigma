from ModernEnigma import ModernEnigma

class Level(object):
    def __init__(self,baseMachineStg,levelMachineStg):
        self.baseStg=baseMachineStg
        self.levelStg=levelMachineStg
        self.inputMsg=""
        self.outputMsg=""
        self.i={0:[],1:[]}
        self.j={0:[],1:[]}
        self.k={0:[],1:[]}
        self.l={0:[],1:[]}
        self.s={0:[],1:[]}
        self.st={0:[],1:[]}

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
        return result
