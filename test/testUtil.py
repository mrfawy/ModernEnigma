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
    def testEncodeStringIntoBytsList(self):
        msg="helLo World!!"
        result=Util.encodeStringIntoByteList(msg)
        self.assertEqual([104, 101, 108, 76, 111, 32, 87, 111, 114, 108, 100, 33, 33],result)

    def testConvertByteListIntoHexString(self):
        l=[104, 101, 108, 76, 111, 32, 87, 111, 114, 108, 100, 33, 33]
        self.assertEqual("68656C4C6F20576F726C642121",Util.convertByteListIntoHexString(l))

    def testConvertHexStringIntoByteList(self):
        string="68656C4C6F20576F726C642121"
        result=[104, 101, 108, 76, 111, 32, 87, 111, 114, 108, 100, 33, 33]
        self.assertEqual(result,Util.convertHexStringIntoByteList(string))

    def testDecodeListtoString(self):
        l=[72, 101, 108, 108, 111, 32, 69, 110, 105, 103, 109, 97, 32, 33]
        self.assertEqual("Hello Enigma !",Util.decodeByteListIntoString(l))



    def testHashing(self):
        hashed=Util.hashString("My String")
        print(hashed)
        self.assertIsNotNone(hashed)

    def testWriteObjectToFileAsJosn(self):
        obj=[1,2,3]
        testFile="testWriteTofile.txt"
        Util.writeObjectToFileAsJson(obj,testFile)

        res=Util.readJsonFileIntoObject(testFile)
        self.assertEqual(obj,res)

    def testDivideIntoChunks(self):
        seq=[0,1,2,3,4,5,6,7,8,9]
        expected=[[0,1],[2,3],[4,5],[6,7],[8,9]]
        res=Util.divideIntoChunks(seq,2)
        self.assertEqual(expected,res)



