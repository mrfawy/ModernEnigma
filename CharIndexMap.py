class CharIndexMap(object):
    rangeTypeisCharacterBased=False
    charRange= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","!","$","#","%","<",">","=","[","]",".",",",";",":","'","\"","?","(",")","&","|","~","-","+","*","/","\\","@","^"]
    binaryRangeSize=2**(1*8) # 2 bytes long range
    binaryRangeSize=10

    lastReturnedRange=None

    @classmethod
    def getRange(cls):
        if cls.lastReturnedRange:
            return cls.lastReturnedRange
        result=[]
        if cls.rangeTypeisCharacterBased:
            result=range(0,len(cls.charRange))
        else:
            result=range(cls.binaryRangeSize)
        cls.lastReturnedRange=result
        print(result)
        return result

    @classmethod
    def getRangeSize(cls):
        return len(cls.getRange())

