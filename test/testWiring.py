import unittest
from Wiring import Wiring

class TestWiring(unittest.TestCase):
    def setUp(self):
        self.config={
            "0": [
                0
            ],
            "1": [
                2
            ],
            "2": [
                1,0
            ]
        }

    def testConnectByConfig(self):
        w=Wiring(self.config)
        self.assertIsNotNone(w)
        self.assertEqual(0,w.getPairedPin(0))
        self.assertEqual(1,w.getPairedPin(2))
        self.assertEqual(2,w.getPairedPin(1))

    def testGetPairedPin(self):
        w=Wiring(self.config)
        self.assertEqual(2,w.getPairedPin(1))

    def testGetPairedPinRev(self):
        w=Wiring(self.config)
        self.assertEqual(2,w.getPairedPinRev(1))

    def testGetMultiPairedPin(self):
        w=Wiring(self.config)
        self.assertEqual(2,len(w.getMultiPairdPin(2)))
        self.assertTrue(0 in w.getMultiPairdPin(2))
        self.assertTrue(1 in w.getMultiPairdPin(2))
    def testExtractAsMap(self):
        w=Wiring(self.config)
        asMap=w.extractAsMap()
        self.assertEqual(3,len(asMap))
        self.assertEqual(2,len(asMap[2]))

