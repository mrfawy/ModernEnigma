from RandomGenerator import RandomGenerator
from Util import Util


#This class implements  Fisher-Yates shuffle algorithm
#Given random generator and a seed , it de/shuffles a string
#http://stackoverflow.com/questions/3541378/reversible-shuffle-algorithm-using-a-key
class Shuffler(object):

    @classmethod
    def shuffleSeq(cls,sequence,seed):
        seq=list(sequence)
        random=RandomGenerator(Util.hashString(str(seed)))
        for i in range(len(seq)-1,0,-1):
           j=random.nextInt(0,i)
           cls.swap(seq,i,j)
        return seq

    @classmethod
    def deshuffleSeq(cls,sequence,seed):
        seq=list(sequence)
        random=RandomGenerator(Util.hashString(str(seed)))
        changes=[]
        for i in range(len(seq)-1,0,-1):
           changes.append(random.nextInt(0,i))
        changes=changes[::-1]
        for i in range(1,len(seq)):
           cls.swap(seq,i,changes[i-1])

        return seq

    @classmethod
    def swap(cls,seq,i,j):
        tmp=seq[i]
        seq[i]=seq[j]
        seq[j]=tmp
