'''
Created on 23-Jul-2012

@author: nbprashanth
'''

import Upstream
import urllib2
import sys
import CustomURL
from WebParse import WebParse

def run():
    
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
            upstream=Upstream.HTTPLS(pkgname, url)
            (ver,loc) = upstream.process()
            print 'Latest version of ' + pkgname + ' is : ' + ver
            
        if method=='dualhttpls':
            upstream=Upstream.DualHTTPLS(pkgname, url)
            (ver,loc) = upstream.process()
            print 'Latest version of ' + pkgname + ' is : ' + ver
            
        if method=='lp':
            upstream=Upstream.Launchpad(pkgname, url)
            (ver,loc) = upstream.process()
            print 'Latest version of ' + pkgname + ' is : ' + ver
            
        if method=='svnls':
            upstream=Upstream.SVNLS(pkgname, url)
            (ver,loc) = upstream.process()
            print 'Latest version of ' + pkgname + ' is : ' + ver
            
        if method=='google':
            upstream=Upstream.Google(pkgname, url)
            (ver,loc) = upstream.process()
            print 'Latest version of ' + pkgname + ' is : ' + ver
            
        if method=='ftpls':
            upstream=Upstream.FTPLS(pkgname, url)
            (ver,loc) = upstream.process()
            print 'Latest version of ' + pkgname + ' is : ' + ver
            
        if method=='trac':
            upstream=Upstream.Trac(pkgname, url)
            (ver,loc) = upstream.process()
            print 'Latest version of ' + pkgname + ' is : ' + ver
            
        if method=='sf':
            upstream=Upstream.SF(pkgname, url)
            (ver,loc) = upstream.process()
            print 'Latest version of ' + pkgname + ' is : ' + ver
            
        if method=='custom':
            custom=CustomURL.CustomURL()
            (ver, loc) = custom.process(url)
            print 'Latest version of ' + pkgname + ' is : ' + ver
            
            
        wp.updateRecord('error', str(error).lower(), id)
        wp.updateRecord('processed', 'true', id)
        wp.updateRecord('latest_ver', ver, id)
        wp.updateRecord('loc', loc, id)
        
if __name__ == '__main__':
    run()