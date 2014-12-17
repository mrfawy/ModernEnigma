import unittest
from EnigmaDynamicFactory import EnigmaDynamicFactory


class TestEnigmaDynamicFactory(unittest.TestCase):
    def setUp(self):
        self.factory=EnigmaDynamicFactory()

    def testCreateSwappingSeparator(self):
        fromRange=[0,1,2,3,4,5,6,7,8,9]
        toRange=[0,1,2]
        separatorConfig=self.factory.createSwappingSeparatorConfig("ID",len(toRange),len(fromRange))
        wiringMap=separatorConfig["wiring"]
        for f in fromRange:
            self.assertTrue(self.existsInKeys(f,wiringMap))
        for t in toRange:
            self.assertTrue(self.existsInValues(t,wiringMap))

    def existsInValues(self,x,wiringMap):
        exists=False
        for pinIn,poutList in wiringMap.items():
            if x in poutList:
                return True
        return exists
    def existsInKeys(self,x,wiringMap):
        exists=False
        for pinIn,poutList in wiringMap.items():
            if x == pinIn:
                return True
        return exists

    def testCreateSwappingLevel2RotorConfig(self):
        level2RotorConfig=self.factory.createSwappingLevel2RotorConfig("id",6)
        self.assertEqual(6,len(level2RotorConfig["wiring"]))

