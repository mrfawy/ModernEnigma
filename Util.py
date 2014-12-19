from CharIndexMap import CharIndexMap
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

