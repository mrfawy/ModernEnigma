import unittest
from StreamConverter import CharacterStreamConverter

class testStreamConverter(unittest.TestCase):
    def testCharConvertInput(self):
        msg="AAAA"
        out=CharacterStreamConverter().convertInput(msg)
        self.assertEqual(4,len(out))
        for o in out:
            self.assertEqual(65,o)
    def testCharConvertOutput(self):
        stream=[65,65,65,65]
        out=CharacterStreamConverter().convertOutput(stream)
        self.assertEqual("AAAA",out)

