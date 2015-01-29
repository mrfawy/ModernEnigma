import unittest
from Shuffler import Shuffler
from Util import Util

class TestShuffler(unittest.TestCase):

    # preparing to test
    def setUp(self):
        self.shuffler=Shuffler()

    def testShuffle(self):
        seq=[0,1,2]
        shSeq=self.shuffler.shuffleSeq(seq,123)
        self.assertNotEqual(seq,shSeq)
        self.assertEqual(len(seq),len(shSeq))

    def testDeshuffle(self):
        shSeq=[3,4,1,5,2,0]
        seq=self.shuffler.deshuffleSeq(shSeq,123)
        self.assertNotEqual(shSeq,seq)
        self.assertEqual(len(shSeq),len(seq))

    def testDuality(self):
        msg=[0,1,2,3,4,5]
        smsg=self.shuffler.shuffleSeq(msg,123)
        dmsg=self.shuffler.deshuffleSeq(smsg,123)
        self.assertEqual(msg,dmsg)
