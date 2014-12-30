import unittest
from Util import Util

class TestUtil(unittest.TestCase):
    def testConvertTupleListToMap(self):
        tupleList=[]
        tupleList.append((0,0))
        tupleList.append((0,1))
        tupleList.append((1,0))
        tupleList.append((1,2))
        tupleList.append((2,2))
        wiringMap=Util.convertTupleListToMap(tupleList)
        self.assertEqual(3,len(wiringMap))
        self.assertEqual(2,len(wiringMap[0]))
        self.assertEqual(1,len(wiringMap[2]))

    def testPadSequence(self):
        seq=[1,2]
        blkSize=4
        padSeq=Util.padSequence(seq,4)
        self.assertEqual(0,len(padSeq)%4)
        self.assertEqual(1,padSeq[0])
    def testPaddingBlksizeLargeerThanSeq(self):
        seq=[1,2]
        blkSize=16
        padSeq=Util.padSequence(seq,blkSize)
        self.assertEqual(0,len(padSeq)%blkSize)
        self.assertEqual(13,padSeq[0])
    def testUnpadSequence(self):
        seq=[1,2,3,4]
        unPadSeq=Util.unpadSequence(seq)
        self.assertEqual(2,len(unPadSeq))
        self.assertEqual([2,3],unPadSeq)

    def testRemoveDuplicates(self):
        seq=[1,2,1,3,1,3,4]
        self.assertEqual([1,2,3,4],Util.removeDuplicates(seq))
    def testHashing(self):
        self.assertIsNotNone(Util.hashString("My String"))

