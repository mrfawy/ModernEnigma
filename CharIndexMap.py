class CharIndexMap(object):
    def __init__(self):
        self.charIndex=[]
        self.load()

    def load(self):
        for char in self.getRange():
            self.charIndex.append(char)

    def getRange(self):
        return ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","!","$","#","%","<",">","=","[","]",".",",",";",":","'","\"","?","(",")","&","|","~","-","+","*","/","\\","@","^"]

    def getRangeSize(self):
        return len(self.charIndex)

    def charToIndex(self,char):
        return self.charIndex.index(char)

    def indexToChar(self,index):
        return self.charIndex[index]


