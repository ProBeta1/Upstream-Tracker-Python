'''
Created on 23-Jul-2012

@author: nbprashanth
'''

import Upstream
import urllib2
import sys
import CustomURL
import threading
import time
from WebParse import WebParse

class Tracker(threading.Thread):
    
    count=0
    limit=1
    timeout=5 #seconds

    def run(self):
        
        wp = WebParse('http://localhost','3000')
        records=wp.getRecords()
        
        if records==None:
            print 'No records found!'
            sys.exit(1)
        
        for record in records:
            
            pkgname=record['pkgname']
            method=record['method']
            url=record['url']
            id=record['id']
            
            error=False
            errorMsg=''
            
            if method=='httpls':
                print 'Latest version of ' + pkgname + ' is : ',
                upstream=Upstream.HTTPLS(pkgname, url)
                (ver,loc) = upstream.process()
                print ver
                
            if method=='dualhttpls':
                print 'Latest version of ' + pkgname + ' is : ',
                upstream=Upstream.DualHTTPLS(pkgname, url)
                (ver,loc) = upstream.process()
                print ver
                
            if method=='lp':
                print 'Latest version of ' + pkgname + ' is : ',
                upstream=Upstream.Launchpad(pkgname, url)
                (ver,loc) = upstream.process()
                print ver
                
            if method=='svnls':
                print 'Latest version of ' + pkgname + ' is : ',
                upstream=Upstream.SVNLS(pkgname, url)
                (ver,loc) = upstream.process()
                print ver
                
            if method=='google':
                print 'Latest version of ' + pkgname + ' is : ',
                upstream=Upstream.Google(pkgname, url)
                (ver,loc) = upstream.process()
                print ver
                
            if method=='ftpls':
                print 'Latest version of ' + pkgname + ' is : ',
                upstream=Upstream.FTPLS(pkgname, url)
                (ver,loc) = upstream.process()
                print ver
                
            if method=='trac':
                print 'Latest version of ' + pkgname + ' is : ',
                upstream=Upstream.Trac(pkgname, url)
                (ver,loc) = upstream.process()
                print ver
                
            if method=='sf':
                print 'Latest version of ' + pkgname + ' is : ',
                upstream=Upstream.SF(pkgname, url)
                (ver,loc) = upstream.process()
                print ver
                
            if method=='custom':
                print 'Latest version of ' + pkgname + ' is : ',
                custom=CustomURL.CustomURL()
                (ver, loc) = custom.process(url)
                print ver
                
            if ver==None:
                error=True
                
            wp.updateRecord('error', str(error).lower(), id)
            wp.updateRecord('processed', 'true', id)
            wp.updateRecord('latest_ver', ver, id)
            wp.updateRecord('loc', loc, id)
            
            self.count+=1
            if self.count%self.limit==0:
                print 'Waiting ' + str(self.timeout) + ' seconds...'
                time.sleep(self.timeout) 
            
        
if __name__ == '__main__':
    tracker=Tracker()
    tracker.start()
