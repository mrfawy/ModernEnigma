class CharIndexMap(object):
    range= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","!","$","#","%","<",">","=","[","]",".",",",";",":","'","\"","?","(",")","&","|","~","-","+","*","/","\\","@","^"]
    charIndex=[]
    for char in range:
        charIndex.append(char)

    @classmethod
    def getRange(cls):

        return cls.range

    @classmethod
    def getRangeSize(cls):
        return len(cls.charIndex)

    @classmethod
    def charToIndex(cls,char):
        return cls.charIndex.index(char)

    @classmethod
    def indexToChar(cls,index):
        return cls.charIndex[index]
# print(CharIndexMap.getRange())
# print(CharIndexMap.getRangeSize())
# print(CharIndexMap.indexToChar(0))
# print(CharIndexMap.charToIndex("A"))
