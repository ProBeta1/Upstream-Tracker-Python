'''
Created on Jun 24, 2012

@author: N.B
'''

import Record
import sys
import Upstream
from Upstream import HTTPLS
from test.test_binop import isnum
import urllib2
from WebParse import WebParse

if __name__ == '__main__':
    
#    filename='upstream.txt'
#    debug=False
#    
#    try:
#        records=Record.Record(filename).getRecords()
#        if debug:
#            print 'Records : ',
#            print records
#    except IOError as e:
#        if e[0]==2:
#            print 'Cannot find file ' + filename
#        else:
#            print 'Error in reading records from file'
#        sys.exit(1)
#        
#    for record in records:
#        
#        pkgname=record[0]
#        method=record[1]
#        url=record[2]

    import WebParse
    wp = WebParse.WebParse('http://localhost','3000')
    records=wp.getRecords()
    
    for record in records:
        
#        if record['processed']=='false':
        
            pkgname=record['pkgname']
            method=record['method']
            url=record['url']
            id=record['id']
            
            if method=='httpls':
                print 'Latest Version (' + pkgname + '): ',
                try:
                    (latestVer, path, error, errorMsg) = Upstream.HTTPLS(pkgname, url).process(False)
                    print latestVer
                except:
                    print 'Can\'t find version'
                    latestVer=None
                    path=None
                    error=True
                    errorMsg='Unknown Error'
                    
                wp.updateRecord('latest_ver', latestVer, str(id))
                wp.updateRecord('processed', 'true', str(id))
                wp.updateRecord('error', str(error).lower(), str(id))
                wp.updateRecord('errorMessage', errorMsg, str(id))

            if method=='dualhttpls':
                print 'Latest Version (' + pkgname + '): ',
                try:
                    (latestVer, path, error, errorMsg) = Upstream.DualHTTPLS(pkgname, url).process(False)
                    print latestVer
                except:
                    print 'Can\'t find version'
                    latestVer=None
                    path=None
                    error=True
                    errorMsg='Unknown Error'
                    
                wp.updateRecord('latest_ver', latestVer, str(id))
                wp.updateRecord('processed', 'true', str(id))
                wp.updateRecord('error', str(error).lower(), str(id))
                wp.updateRecord('errorMessage', errorMsg, str(id))
                    

                
            if method=='lp':
                print 'Latest Version (' + pkgname + '): ',
                try:
                    (latestVer, path, error, errorMsg) = Upstream.Launchpad(pkgname, url).process(False)
                    print latestVer
                except:
                    print 'Can\'t find version'
                    latestVer=None
                    path=None
                    error=True
                    errorMsg='Unknown Error'
                    
                wp.updateRecord('latest_ver', latestVer, str(id))
                wp.updateRecord('processed', 'true', str(id))
                wp.updateRecord('error', str(error).lower(), str(id))
                wp.updateRecord('errorMessage', errorMsg, str(id))

            if method=='svnls':
                print 'Latest Version (' + pkgname + '): ',
                try:
                    (latestVer, path, error, errorMsg) = Upstream.SVNLS(pkgname, url).process(False)
                    print latestVer
                except:
                    print 'Can\'t find version'
                    latestVer=None
                    path=None
                    error=True
                    errorMsg='Unknown Error'
                    
                wp.updateRecord('latest_ver', latestVer, str(id))
                wp.updateRecord('processed', 'true', str(id))
                wp.updateRecord('error', str(error).lower(), str(id))
                wp.updateRecord('errorMessage', errorMsg, str(id))

                
            if method=='google':
                print 'Latest Version (' + pkgname + '): ',
                try:
                    (latestVer, path, error, errorMsg) = Upstream.Google(pkgname, url).process(False)
                    print latestVer
                except:
                    print 'Can\'t find version'
                    latestVer=None
                    path=None
                    error=True
                    errorMsg='Unknown Error'
                    
                wp.updateRecord('latest_ver', latestVer, str(id))
                wp.updateRecord('processed', 'true', str(id))
                wp.updateRecord('error', str(error).lower(), str(id))
                wp.updateRecord('errorMessage', errorMsg, str(id))

            if method=='ftpls':
                print 'Latest Version (' + pkgname + '): ',
                try:
                    (latestVer, path, error, errorMsg) = Upstream.FTPLS(pkgname, url).process(False)
                    print latestVer
                except:
                    print 'Can\'t find version'
                    latestVer=None
                    path=None
                    error=True
                    errorMsg='Unknown Error'
                    
                wp.updateRecord('latest_ver', latestVer, str(id))
                wp.updateRecord('processed', 'true', str(id))
                wp.updateRecord('error', str(error).lower(), str(id))
                wp.updateRecord('errorMessage', errorMsg, str(id))

            if method=='trac':
                print 'Latest Version (' + pkgname + '): ',
                try:
                    (latestVer, path, error, errorMsg) = Upstream.Trac(pkgname, url).process(False)
                    print latestVer
                except:
                    print 'Can\'t find version'
                    latestVer=None
                    path=None
                    error=True
                    errorMsg='Unknown Error'
                    
                wp.updateRecord('latest_ver', latestVer, str(id))
                wp.updateRecord('processed', 'true', str(id))
                wp.updateRecord('error', str(error).lower(), str(id))
                wp.updateRecord('errorMessage', errorMsg, str(id))

                
            if method=='subdirhttpls':
                print 'Latest Version (' + pkgname + '): ',
                try:
                    (latestVer, path, error, errorMsg) = Upstream.SubdirHTTPLS(pkgname, url).process(False)
                    print latestVer
                except:
                    print 'Can\'t find version'
                    latestVer=None
                    path=None
                    error=True
                    errorMsg='Unknown Error'
                    
                wp.updateRecord('latest_ver', latestVer, str(id))
                wp.updateRecord('processed', 'true', str(id))
                wp.updateRecord('error', str(error).lower(), str(id))
                wp.updateRecord('errorMessage', errorMsg, str(id))
