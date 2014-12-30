import unittest
from CharIndexMap import CharIndexMap
from StreamConverter import CharacterStreamConverter
from StreamConverter import ByteStreamConverter

class testStreamConverter(unittest.TestCase):
    def setUp(self):
        CharIndexMap.rangeTypeisCharacterBased=True
    def testCharConvertInput(self):
        msg="AAAA"
        out=CharacterStreamConverter().convertInput(msg)
        self.assertEqual(4,len(out))
        for o in out:
            self.assertEqual(0,o)
    def testCharConvertOutput(self):
        stream=[0,0,0,0]
        out=CharacterStreamConverter().convertOutput(stream)
        self.assertEqual("AAAA",out)

    def testByteStreamConverter(self):
        result=ByteStreamConverter().convertInput([9,3,1,1,0,0],8)
        self.assertEqual(3,len(result))
        self.assertEqual([[0,3],[6,7]],result[0])
        self.assertEqual([[],[]],result[2])


