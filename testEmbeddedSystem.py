import unittest
import EmbbedSystem


class MyTestCase(unittest.TestCase):
    def testRetreiveData(self):
        self.assertEqual(EmbbedSystem.RetreiveData(), True)
if __name__ == '__main__':
    unittest.main()