from random import Random
from CharIndexMap import CharIndexMap

"""This class is to abstract random generation , as Per protocol specs we will need to implement certain Secure Random Generator
for now it just wrapps python Random Class which is based on PRNG of Mersenne twister """
class RandomGenerator(object):
    def __init__(self,seed=None):
        self.random=Random()
        if seed:
            self.random.seed(seed)

    def seed(self,seed):
        self.random.seed(seed)

    def sample(self,seq,k):
        return self.random.sample(seq,k)

    def nextInt(self,a=0,b=None):
        if not b:
            b=CharIndexMap.getRangeSize()-1
        return self.random.randint(a,b)
