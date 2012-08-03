'''
Created on Aug 2, 2012

@author: Prashanth
'''

from Upstream import Upstream, HTTPLS, FTPLS, Google, Launchpad, SVNLS, Trac,\
    SubdirHTTPLS, DualHTTPLS, Custom
from WebParse import WebParse
import sys

if __name__ == '__main__':
    
#    Uncomment the following lines to test
        
#    upstream=HTTPLS('http://coherence.beebits.net/download/', 'Coherence')
#    (latestVer, location, error)=upstream.process()
#    print latestVer, location, error
#    
#    upstream=FTPLS('ftp://ftp.gimp.org/pub/gimp/help/', 'gimp-help')
#    (latestVer, location, error)=upstream.process()
#    print latestVer, location, error
#    
#    upstream=Google('giver', 'giver')
#    (latestVer, location, error)=upstream.process()
#    print latestVer, location, error
#    
#    upstream=Launchpad('dee', 'dee')
#    (latestVer, location, error)=upstream.process()
#    print latestVer, location, error
#    
#    upstream=SVNLS('https://svn.revolutionlinux.com/MILLE/XTERM/trunk/libflashsupport/Tarballs/', 'libflashsupport')
#    (latestVer, location, error)=upstream.process()
#    print latestVer, location, error
#    
#    upstream=Trac('http://guake.org/downloads', 'guake')
#    (latestVer, location, error)=upstream.process()
#    print latestVer, location, error
#    
#    upstream=SubdirHTTPLS('http://ftp.gtk.org/pub/babl/', 'babl')
#    (latestVer, location, error)=upstream.process()
#    print latestVer, location, error
#    
#    upstream=Custom('http://www.abisource.com/downloads/abiword/([\d\.]+)/source/abiword-([\d\.]+)\.tar\.gz', 'abiword')
#    (latestVer, location, error)=upstream.process()
#    print latestVer, location, error
#    
#    upstream=Custom('ftp://ftp.kde.org/pub/kde/unstable/amarok/([0-9.]+)/src/amarok-([\d\.]+)\.tar\.bz2', 'amarok')
#    (latestVer, location, error)=upstream.process()
#    print latestVer, location, error
#
#    upstream=Custom('http://code.google.com/p/chmsee/downloads/list/chmsee-([\d\.]+)\.tar\.gz', 'chmsee')
#    (latestVer, location, error)=upstream.process()
#    print latestVer, location, error

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
        
        errorMsg=''
        
        if method=='httpls':
            print 'Latest version of ' + pkgname + ' is : ',
            upstream=HTTPLS(url, pkgname)
            (ver,loc,error) = upstream.process()
            print ver
            
        if method=='dualhttpls':
            print 'Latest version of ' + pkgname + ' is : ',
            upstream=DualHTTPLS(url, pkgname)
            (ver,loc,error) = upstream.process()
            print ver
            
        if method=='lp':
            print 'Latest version of ' + pkgname + ' is : ',
            upstream=Launchpad(url, pkgname)
            (ver,loc,error) = upstream.process()
            print ver
            
        if method=='svnls':
            print 'Latest version of ' + pkgname + ' is : ',
            upstream=SVNLS(url, pkgname)
            (ver,loc,error) = upstream.process()
            print ver
            
        if method=='google':
            print 'Latest version of ' + pkgname + ' is : ',
            upstream=Google(url, pkgname)
            (ver,loc,error) = upstream.process()
            print ver
            
        if method=='ftpls':
            print 'Latest version of ' + pkgname + ' is : ',
            upstream=FTPLS(url, pkgname)
            (ver,loc,error) = upstream.process()
            print ver
            
        if method=='trac':
            print 'Latest version of ' + pkgname + ' is : ',
            upstream=Trac(url, pkgname)
            (ver,loc,error) = upstream.process()
            print ver
            
        if method=='sf':
            print 'Latest version of ' + pkgname + ' is : ',
            upstream=SF(url, pkgname)
            (ver,loc,error) = upstream.process()
            print ver
            
        if method=='custom':
            print 'Latest version of ' + pkgname + ' is : ',
            custom=Custom(url, pkgname)
            (ver,loc,error) = custom.process()
            print ver
            
        if error==None:
            error=False
            errorMsg=''
        else:
            errorMsg=error
            error=True
            
            
        wp.updateRecord('error', str(error).lower(), id)
        wp.updateRecord('errorMessage', errorMsg, id)
        wp.updateRecord('processed', 'true', id)
        wp.updateRecord('latest_ver', ver, id)
        wp.updateRecord('loc', loc, id)
    
#    