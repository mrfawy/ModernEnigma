from CharIndexMap import CharIndexMap

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

