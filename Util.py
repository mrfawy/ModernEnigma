from CharIndexMap import CharIndexMap
from RandomGenerator import RandomGenerator
import json
import codecs
import hashlib

class Util(object):

    @classmethod
    def seqToStr(cls,seq):
        result=""
        for c in seq:
            result+=c
        return result

    @classmethod
    def strToSeq(cls,string):
        result=[]
        for c in string:
            result.append(c)

        return result
    @classmethod
    def convertTupleListToMap(cls,wiringTuples):
        wiringCfg={}
        for t in wiringTuples:
            fromPin=t[0]
            toPin=t[1]
            if fromPin not in wiringCfg:
                wiringCfg[fromPin]=[]
            wiringCfg[fromPin].append(toPin)
        return wiringCfg
    @classmethod
    def toJson(cls,obj):
        return (json.dumps(obj,sort_keys=True,indent=4, separators=(',', ': ')))

    @classmethod
    def padSequence(cls,seq,blkSize,seed=None):
        random=RandomGenerator(seed)
        result=list(seq)
        result.insert(0,0)
        rem=len(result)%blkSize
        if rem >0:
            sampleSize=blkSize-rem
            if sampleSize>len(result):
                for i in range(sampleSize):
                    byteRange=range(256)
                    result.append(random.sample(byteRange,1)[0])
            else:
                result=result+random.sample(result,sampleSize)
            result[0]=sampleSize
        return result
    @classmethod
    def unpadSequence(cls,seq):
        if seq[0]==0:
            return list(seq[1::])
        else:
            return list(seq[1:len(seq)-seq[0]])

    @classmethod
    def removeDuplicates(cls,seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if not (x in seen or seen_add(x))]

    @classmethod
    def hashString(cls,string,salt=None):
        hashed=hashlib.sha512(string.encode("utf_8")).hexdigest()
        return hashed

    @classmethod
    def encodeStringIntoByteList(cls,string,encoding="utf_8"):
        return list(codecs.encode(string,encoding))
    @classmethod
    def decodeByteListIntoString(cls,byteList,encoding="utf_8"):
        result=""
        for s in byteList:
            x=''.join('{:02X}'.format(s))
            result+=bytes.fromhex(x).decode(encoding)
        return result
    @classmethod
    def convertByteListIntoHexString(cls,byteList):
        resultStr=''.join('{:02X}'.format(a) for a in byteList)
        return resultStr
    @classmethod
    def convertHexStringIntoByteList(cls,string):
        return list(bytes.fromhex(string))

    @classmethod
    def writeObjectToFileAsJson(cls,obj,fileName):
        target = open(fileName, 'w')
        target.write(Util.toJson(obj))
        target.close()
    @classmethod
    def readJsonFileIntoObject(cls,fileName):
        target = open(fileName, 'r')
        fileContents=target.read()
        target.close()
        return  json.loads(fileContents)






