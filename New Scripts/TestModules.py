'''
Created on 25-Jul-2012

@author: nbprashanth
'''
import unittest
from Upstream import *

class TestModules(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        
    def test_HTTPLS(self):
        upstream=HTTPLS('Coherence','http://coherence.beebits.net/download/')
        self.failIfEqual(upstream.process(), (None, None), 'Failed HTTPLS test.')
        
    def test_DualHTTPLS(self):
        upstream=DualHTTPLS('cairo','http://cairographics.org/snapshots/|http://cairographics.org/releases/')
        self.failIfEqual(upstream.process(), (None, None), 'Failed DualHTTPLS test.')
        
    def test_Launchpad(self):
        upstream=Launchpad('dee','dee')
        self.failIfEqual(upstream.process(), (None, None), 'Failed Launchpad test.')
        
    def test_SVNLS(self):
        upstream=SVNLS('libflashsupport','https://svn.revolutionlinux.com/MILLE/XTERM/trunk/libflashsupport/Tarballs/')
        self.failIfEqual(upstream.process(), (None, None), 'Failed SVNLS test.')
        
    def test_Google(self):
        upstream=Google('liblouis','liblouis')
        self.failIfEqual(upstream.process(), (None, None), 'Failed Google test.')
        
    def test_FTPLS(self):
        upstream=FTPLS('mtr','ftp://ftp.bitwizard.nl/mtr/')
        self.failIfEqual(upstream.process(), (None, None), 'Failed FTPLS test.')
        
    def test_Trac(self):
        upstream=Trac('guake','http://guake.org/downloads')
        self.failIfEqual(upstream.process(), (None, None), 'Failed Trac test.')
        
    def test_SF(self):
        upstream=SF('ht','1066')
        self.failIfEqual(upstream.process(), (None, None), 'Failed Sourceforge test.')
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    print 'Testing basics using sample records.\n'
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModules)
    unittest.TextTestRunner(verbosity=2).run(suite)