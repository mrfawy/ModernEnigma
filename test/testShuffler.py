import unittest
from Shuffler import Shuffler
from Util import Util

class TestShuffler(unittest.TestCase):

    # preparing to test
    def setUp(self):
        self.shuffler=Shuffler()

    def testShuffle(self):
        seq=["A","B","C"]
        shSeq=self.shuffler.shuffleSeq(seq,123)
        self.assertNotEqual(seq,shSeq)
        self.assertEqual(len(seq),len(shSeq))

    def testDeshuffle(self):
        shSeq=Util.strToSeq("debfca")
        seq=self.shuffler.deshuffleSeq(shSeq,123)
        self.assertNotEqual(shSeq,seq)
        self.assertEqual(len(shSeq),len(seq))
        self.assertEqual(Util.seqToStr(seq),"abcdef")

    def testDuality(self):
        msg=Util.strToSeq("abcdef")
        smsg=self.shuffler.shuffleSeq(msg,123)
        dmsg=self.shuffler.deshuffleSeq(smsg,123)
        self.assertEqual(msg,dmsg)
