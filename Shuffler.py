from random import Random


#This class implements  Fisher-Yates shuffle algorithm
#Given random generator and a seed , it de/shuffles a string
#http://stackoverflow.com/questions/3541378/reversible-shuffle-algorithm-using-a-key
class Shuffler(object):
    def __init__(self,random=None):
        if random:
            self.random=random
        else:
            self.random=Random()

    def shuffle(self,msg,seed):
        self.random.seed(seed)
        msgSeq=self.strToSeq(msg)
        for i in range(len(msgSeq)-1,0,-1):
           j=self.random.randint(0,i)
           self.swap(msgSeq,i,j)
        return self.SeqToStr(msgSeq)

    def deshuffle(self,msg,seed):
        self.random.seed(seed)
        msgSeq=self.strToSeq(msg)
        changes=[]
        for i in range(len(msgSeq)-1,0,-1):
           changes.append(self.random.randint(0,i))
        changes=changes[::-1]
        for i in range(1,len(msgSeq)):
           self.swap(msgSeq,i,changes[i-1])

        return self.SeqToStr(msgSeq)


    def swap(self,seq,i,j):
        tmp=seq[i]
        seq[i]=seq[j]
        seq[j]=tmp
    def strToSeq(self,s):
        result=[]
        for c in s:
            result.append(c)
        return result
    def SeqToStr(self,seq):
        result=""
        for c in seq:
            result+=c
        return result

# m="abcdef"
# s=Shuffler()
# ms=s.shuffle(m,123)
# print(m)
# print(ms)
# print(s.deshuffle(ms,123))
