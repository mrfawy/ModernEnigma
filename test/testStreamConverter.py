import unittest
from CharIndexMap import CharIndexMap
from StreamConverter import CharacterStreamConverter

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

