'''
Created on 25-Jul-2012

@author: nbprashanth
'''
import unittest
from CustomURL import CustomURL 

class TestCustomURL(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        
    def test_cutsomURL(self):
        custom=CustomURL()
        (latestVer, url) = custom.process('http://pan.rebelbase.com/download/releases/(.*)/source/pan-((\d\.*)+).tar.bz2')
        self.failIfEqual(url, (None, None), 'Failed custom URL test.')
        print url, latestVer
        
    def test_customURL_1(self):
        custom=CustomURL()
        (latestVer, url) = custom.process('https://developer.berlios.de/project/showfiles.php?group_id=6784|http://(?:.*)iat-(\d+(?:\.\d+){1,3})-src.tar.(?:bz2|gz)')
        self.failIfEqual(url, (None, None), 'Failed custom URL test.')
        print url, latestVer
        
                 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    print 'Testing Custom URL parsing\n'
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCustomURL)
    unittest.TextTestRunner(verbosity=2).run(suite)