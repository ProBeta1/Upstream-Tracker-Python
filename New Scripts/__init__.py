'''
Created on Jun 24, 2012

@author: N.B
'''

import Record
import sys
import Upstream

if __name__ == '__main__':
    
    filename='upstream.txt'
    debug=False
    
    try:
        records=Record.Record(filename).getRecords()
        if debug:
            print 'Records : ',
            print records
    except IOError as e:
        if e[0]==2:
            print 'Cannot find file ' + filename
        else:
            print 'Error in reading records from file'
        sys.exit(1)
        
    for record in records:
        
        pkgname=record[0]
        method=record[1]
        url=record[2]
        
#        if method=='httpls':
#            print 'Latest Version (' + pkgname + '): ',
#            try:
#                latestVer = Upstream.HTTPLS(pkgname, url).process(False)
#                if latestVer!=None:
#                    print latestVer
#            except:
#                print 'Can\'t find version'
#                pass
            
#        if method=='dualhttpls':
#            print 'Latest Version (' + pkgname + '): ',
#            try:
#                latestVer = Upstream.DualHTTPLS(pkgname, url).process(False)
#                if latestVer!=None:
#                    print latestVer
#            except:
#                print 'Can\'t find version'
#                pass
        
#        if method=='lp':
#            print 'Latest Version (' + pkgname + '): ',
#            try:
#                latestVer = Upstream.Launchpad(pkgname, url).process(False)
#                if latestVer!=None:
#                    print latestVer
#            except:
#                print 'Can\'t find version'
#                pass
            
#        if method=='svnls':
#            print 'Latest Version (' + pkgname + '): ',
#            try:
#                latestVer = Upstream.SVNLS(pkgname, url).process(False)
#                if latestVer!=None:
#                    print latestVer
#            except:
#                print 'Can\'t find version'
#                pass

#        if method=='google':
#            print 'Latest Version (' + pkgname + '): ',
#            try:
#                latestVer = Upstream.Google(pkgname, url).process(False)
#                if latestVer!=None:
#                    print latestVer
#            except:
#                print 'Can\'t find version'
#                pass        
            
#        if method=='ftpls':
#            print 'Latest Version (' + pkgname + '): ',
#            try:
#                latestVer = Upstream.FTPLS(pkgname, url).process(False)
#                if latestVer!=None:
#                    print latestVer
#            except:
#                print 'Can\'t find version'
#                pass        
            
#        if method=='trac':
#            print 'Latest Version (' + pkgname + '): ',
#            try:
#                latestVer = Upstream.Trac(pkgname, url).process(False)
#                if latestVer!=None:
#                    print latestVer
#            except:
#                print 'Can\'t find version'
#                pass
            
        if method=='subdirhttpls':
            print 'Latest Version (' + pkgname + '): ',
            try:
                latestVer = Upstream.SubdirHTTPLS(pkgname, url).process(False)
                if latestVer!=None:
                    print latestVer
            except:
                print 'Can\'t find version'
                pass         