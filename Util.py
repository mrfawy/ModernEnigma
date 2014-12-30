from CharIndexMap import CharIndexMap
from RandomGenerator import RandomGenerator
import json

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
    def padSequence(cls,seq,blkSize):
        result=list(seq)
        result.insert(0,0)
        rem=len(result)%blkSize
        if rem >0:
            sampleSize=blkSize-rem
            if sampleSize>len(result):
                for i in range(sampleSize):
                    result.append(RandomGenerator().nextInt())
            else:
                result=result+RandomGenerator().sample(result,sampleSize)
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
