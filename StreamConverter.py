from CharIndexMap import CharIndexMap
class StreamConverter(object):
    def convertInput(self,inputStream):
        print("no stream converion !!")
        return inputStream

    def convertOutput(self,outputStream):
        print("no stream converion !!")
        return outputStream
class ByteStreamConverter(StreamConverter):
    def convertInput(self,byteStream,blkSize):
        onesMap={0:[],1:[3],2:[2],3:[2,3],4:[1],5:[1,3],6:[1,2],7:[1,2,3],8:[0],9:[0,3],10:[0,2],11:[0,2,3],12:[0,1],13:[0,1,3],14:[0,1,2],15:[0,1,2,3]}
        base=0
        result=[]
        tmp=[]
        for b in byteStream:
            tmp.append([x+base for x in onesMap[b]])
            base=(base+4)%blkSize
            if base%blkSize==0:
                result.append(tmp)
                tmp=[]
        return result

class CharacterStreamConverter(StreamConverter):
    def convertInput(self,inputStream):
        result=[]
        if not isinstance(inputStream,str):
            raise Exception("invalid stream , expecting a string !!")
        for c in inputStream:
            result.append(CharIndexMap.charRange.index(c))
        return result

    def convertOutput(self,outputStream):
        result=""
        for o in outputStream:
            result+=CharIndexMap.charRange[o]
        return result
