import FinalFBnoCam
import unittest
class MyTestCase(unittest.TestCase):


    def testRetreiveData(self):
        itemlist, itemlist_key, CustomerAddress = FinalFBnoCam.RetreiveData()
        self.assertEqual(CustomerAddress,'Aumphur Muang,Chiangmai')
        self.assertEqual(itemlist_key[0],'-KzyX5tD07R7qv87dEdS')
        self.assertEqual(itemlist[0]['price'],30)
    def testCreatArrayKey(self):
        rawString = '"6,17"'

        actualResult = FinalFBnoCam.CreateArrayOfKeyDict(rawString)

        self.assertEqual(actualResult[0],'6')
        self.assertEqual(actualResult[1],'17')

    def testReplaceValues(self):
        rawString = '/"6","17"'
        actualResult = FinalFBnoCam.ReplaceValuesInDict(rawString)
        rawString1 = '"17"'
        actualResult1 = FinalFBnoCam.ReplaceValuesInDict(rawString1)
        self.assertEqual(actualResult,'6'+','+'17')
        self.assertEqual(actualResult1,'17')

    def testUpdate(self):
        a = ['6','17']
        actualResult = FinalFBnoCam.UpdateNewValuesDictKey(a)
        self.assertEqual(actualResult,'6,17')
if __name__ == '__main__':
    unittest.main()
