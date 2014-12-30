from RandomGenerator import RandomGenerator


#This class implements  Fisher-Yates shuffle algorithm
#Given random generator and a seed , it de/shuffles a string
#http://stackoverflow.com/questions/3541378/reversible-shuffle-algorithm-using-a-key
class Shuffler(object):
    def __init__(self,random=None):
        if random:
            self.random=random
        else:
            self.random=RandomGenerator()

    def shuffleSeq(self,sequence,seed=None):
        seq=list(sequence)
        if seed:
            self.random.seed(seed)
        for i in range(len(seq)-1,0,-1):
           j=self.random.nextInt(0,i)
           self.swap(seq,i,j)
        return seq

    def deshuffleSeq(self,sequence,seed=None):
        seq=list(sequence)
        if seed:
            self.random.seed(seed)
        changes=[]
        for i in range(len(seq)-1,0,-1):
           changes.append(self.random.nextInt(0,i))
        changes=changes[::-1]
        for i in range(1,len(seq)):
           self.swap(seq,i,changes[i-1])

        return seq

    def swap(self,seq,i,j):
        tmp=seq[i]
        seq[i]=seq[j]
        seq[j]=tmp
