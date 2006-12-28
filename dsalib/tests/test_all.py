import unittest
from dsalib import dsalib

class MyFirstTestCase(unittest.TestCase):
    def setUp(self):
        self.d = dsalib.DSABase()

    def tearDown(self):
        del self.d

    def testNumberOfItems(self):
        nb_items = self.d.update_base()
        assert nb_items > 1

if __name__ == '__main__':
    main()
