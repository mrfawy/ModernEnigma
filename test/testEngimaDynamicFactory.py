import unittest
from EnigmaDynamicFactory import EnigmaDynamicFactory


class TestEnigmaDynamicFactory(unittest.TestCase):
    def setUp(self):
        self.factory=EnigmaDynamicFactory()

    def testCreateSwappingSeparator(self):
        fromRange=[0,1,2,3,4,5,6,7,8,9]
        toRange=[0,1,2]
        separatorConfig=self.factory.createSwappingSeparatorConfig("ID",len(fromRange),len(toRange))
        tupleList=separatorConfig["wiring"]
        for f in fromRange:
            self.assertTrue(self.existsInTuples(f,tupleList))
        for t in toRange:
            self.assertTrue(self.existsInTuples(t,tupleList))

    def existsInTuples(self,x,tupleList):
        exists=False
        for t in tupleList:
            if x in t:
                return True

    def testCreateSwappingLevel2RotorConfig(self):
        level2RotorConfig=self.factory.createSwappingLevel2RotorConfig("id",6)
        self.assertEqual(6,len(level2RotorConfig["wiring"]))

