import unittest
from Shuffler import Shuffler

class TestShuffler(unittest.TestCase):

    # preparing to test
    def setUp(self):
        self.shuffler=Shuffler()

    def testShuffle(self):
        msg="abcdef"
        smsg=self.shuffler.shuffle(msg,123)
        self.assertNotEqual(msg,smsg)
        self.assertEqual(len(msg),len(smsg))

    def testDeshuffle(self):
        smsg="debfca"
        msg=self.shuffler.deshuffle(smsg,123)
        self.assertNotEqual(msg,smsg)
        self.assertEqual(len(msg),len(smsg))
        self.assertEqual(msg,"abcdef")

    def testDuality(self):
        msg="abcdef"
        smsg=self.shuffler.shuffle(msg,123)
        dmsg=self.shuffler.deshuffle(smsg,123)
        self.assertEqual(msg,dmsg)
