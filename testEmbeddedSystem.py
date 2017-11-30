#import FinalFBnoCam
import FinalProgressWithCam
import unittest
class MyTestCase(unittest.TestCase):


    def testRetreiveData(self):
        itemlist, itemlist_key, CustomerAddress = FinalFBnoCam.RetreiveData()
        self.assertEqual(CustomerAddress,'Aumphur Muang,Chiangmai')
        self.assertEqual(itemlist_key[0],'-KzyX5tD07R7qv87dEdS')
        self.assertEqual(itemlist[0]['price'],30)
    def testCreatArrayKey(self):
        rawString = '"Test1,Test2"'

        actualResult = FinalFBnoCam.CreateArrayOfKeyDict(rawString)

        self.assertEqual(actualResult[0],'Test1')
        self.assertEqual(actualResult[1],'Test2')

    def testReplaceValues(self):
        rawString = '/] Hello ['
        actualResult = FinalFBnoCam.ReplaceValuesInDict(rawString)
        rawString1 = '[]/ M[ e ]t h/ od'
        actualResult1 = FinalFBnoCam.ReplaceValuesInDict(rawString1)
        self.assertEqual(actualResult,'Hello')
        self.assertEqual(actualResult1,'Method')

    def testUpdate(self):
        a = ['Hello','World','by','Python']
        actualResult = FinalFBnoCam.UpdateNewValuesDictKey(a)
        self.assertEqual(actualResult,'Hello,World,by,Python')
if __name__ == '__main__':
    unittest.main()
