class CharIndexMap(object):
    charRange= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","!","$","#","%","<",">","=","[","]",".",",",";",":","'","\"","?","(",")","&","|","~","-","+","*","/","\\","@","^"]

    @classmethod
    def getRange(cls):
        return range(0,len(cls.charRange))

    @classmethod
    def getNonAlphaNumericRange(cls):
        return cls.charRange[cls.charToIndex("!"):len(cls.charRange)]
    @classmethod
    def getFirstNChars(cls,n):
        if n<len(cls.charRange):
            return clas.getRange()[0:n]
        raise("Invaid First N character Range ")

    @classmethod
    def getRangeSize(cls):
        return len(cls.charRange)

    @classmethod
    def charToIndex(cls,char):
        return cls.charRange.index(char)

    @classmethod
    def indexToChar(cls,index):
        return cls.charRange[index]
