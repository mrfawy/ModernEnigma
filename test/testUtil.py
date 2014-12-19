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

