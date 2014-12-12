import unittest
from CharIndexMap import CharIndexMap

class TestShuffler(unittest.TestCase):

    # preparing to test
    def setUp(self):
        pass

    def testGetRange(self):
        self.assertIsNotNone(CharIndexMap.getRange())
        self.assertTrue(CharIndexMap.getRangeSize()==64)

    def testCharIndexMapping(self):
        index=CharIndexMap.charToIndex("X")
        char="X"
        self.assertEqual(CharIndexMap.indexToChar(index),char)
