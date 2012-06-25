'''
Created on Jun 24, 2012

@author: N.B
'''

import urllib2
from urllib2 import HTTPError, URLError
import BeautifulSoup
import re

class Upstream(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def getPageData(self, url):
        try:
            data=urllib2.urlopen(url).read()
            return data
#        except HTTPError, e:
#            print 'HTTP Error - '+e.reason
#            return None
        except URLError, e:
            print 'URL Error - '+e.reason
            return None
        
    def getPageLinks(self, data, tag='a', contents=False):
        soup=BeautifulSoup.BeautifulSoup(data)
        soup.prettify()
        
        links=[]
        
        for link in soup.findAll(tag):
            try:
                if contents:
                    tmp=link.contents
                else:
                    tmp=link['href']
                links.append(str(tmp))
            except:
                pass
            
        if len(links)==0:
            return None
        else:
            return links
        
    def getPageVersions(self, links, pkgname):
        
        versions=[]
        
        for link in links:
            if link.find(pkgname)>=0:
                try:
                    matchObj=re.search('^.*'+pkgname+'[_-](([0-9]+[\.\-])*[0-9]+)\.(?:tar.*|t[bg]z2?).*$', str(link))
                    versions.append(matchObj.group(1))
                except:
                    pass
                            
            
        if len(versions)==0:
            return None
        else:
            return versions        
        
    def getLatestVersion(self, versions):
                
        return max(versions)
    
class HTTPLS(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url=url
        
    def process(self, debugBool):
        
        debug=debugBool
    
        data=Upstream.getPageData(self, self.url)
        
        if data==None:
            print 'Unable to read page source'
            return None
            
        links=Upstream.getPageLinks(self, data)
        
        if links==None:
            print 'Unable to find links on page'
            return None
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            print 'Unable to extract version string'
            return None
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            print 'Unable to obtain latest version'
            return None
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        return latestVer
    
class DualHTTPLS(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url1=url.split('|')[0]
        self.url2=url.split('|')[1]
        
    def process(self, debugBool):
        
        debug=debugBool
        
        data1=Upstream.getPageData(self, self.url1)
        
        data2=Upstream.getPageData(self, self.url2)
        
        data=data1+data2
        
        if data1==None and data2==None:
            print 'Unable to read page source'
            return None
            
        links=Upstream.getPageLinks(self, data)
        
        if links==None:
            print 'Unable to find links on page'
            return None
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            print 'Unable to extract version string'
            return None
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            print 'Unable to obtain latest version'
            return None
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        return latestVer
    
class Launchpad(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url=url
        
    def process(self, debugBool):
        
        debug=debugBool
        
        self.url='http://launchpad.net/'+self.url.strip()+'/+download'
        
        data=Upstream.getPageData(self, self.url)
        
        if data==None:
            print 'Unable to read page source'
            return None
            
        links=Upstream.getPageLinks(self, data)
        
        if links==None:
            print 'Unable to find links on page'
            return None
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            print 'Unable to extract version string'
            return None
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            print 'Unable to obtain latest version'
            return None
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
        
        return latestVer
    
class SVNLS(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url=url
        
    def process(self, debugBool):
        
        debug=debugBool
    
        data=Upstream.getPageData(self, self.url)
        
        if data==None:
            print 'Unable to read page source'
            return None
            
        links=Upstream.getPageLinks(self, data, 'file')
        
        if links==None:
            print 'Unable to find links on page'
            return None
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            print 'Unable to extract version string'
            return None
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            print 'Unable to obtain latest version'
            return None
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        return latestVer

class Google(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url=url
        
    def process(self, debugBool):
        
        debug=debugBool
    
        if self.url.find('|')>=0:
            tarball=self.url.split('|')[1].strip()
            prjname=self.url.split('|')[0].strip()
        else:
            tarball=self.url.strip()
            prjname=self.url.strip()
            
        self.url='http://code.google.com/p/'+prjname.strip()+'/downloads/list'
        
        data=Upstream.getPageData(self, self.url)
        
        if data==None:
            print 'Unable to read page source'
            return None
            
        links=Upstream.getPageLinks(self, data)
        
        if links==None:
            print 'Unable to find links on page'
            return None
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, tarball)
        
        if versions==None:
            print 'Unable to extract version string'
            return None
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            print 'Unable to obtain latest version'
            return None
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        return latestVer

import ftplib
import urlparse

class FTPLS(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname.strip()
        self.url=url.strip()
        
    def process(self, debugBool):
        
        debug=debugBool
    
        files = []
        
        urlparsed=urlparse.urlparse(self.url)
         
        ftp = ftplib.FTP(urlparsed.hostname)
        ftp.login("anonymous", "")
        ftp.cwd(urlparsed.path)

        try:
            files = ftp.nlst()
        except ftplib.error_perm, resp:
            if str(resp) == "550 No files found":
                print "No files in this directory"
            else:
                raise
        
        if files==None:
            print 'Unable to read page source'
            return None
        
        versions=Upstream.getPageVersions(self, files, self.pkgname)
        
        if versions==None:
            print 'Unable to extract version string'
            return None
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            print 'Unable to obtain latest version'
            return None
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        return latestVer

class Trac(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url=url
        
    def process(self, debugBool):
        
        debug=debugBool
    
        data=Upstream.getPageData(self, self.url)
        
        if data==None:
            print 'Unable to read page source'
            return None
            
        links=Upstream.getPageLinks(self, data,'a', True)
        
        if links==None:
            print 'Unable to find links on page'
            return None
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            print 'Unable to extract version string'
            return None
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            print 'Unable to obtain latest version'
            return None
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        return latestVer
    
class SubdirHTTPLS(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url=url
        
    def process(self, debugBool):
        
        debug=debugBool
    
        data=Upstream.getPageData(self, self.url)
        
        if data==None:
            print 'Unable to read page source'
            return None
            
        links=Upstream.getPageLinks(self, data)
        
        if links==None:
            print 'Unable to find links on page'
            return None
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
        
        newLinks=[]
        for link in links:
            try:
                m=re.search('([\d\.]+)',str(link))
                newLinks.append(m.group(0))
            except:
                pass
            
        latestMajorVer=Upstream.getLatestVersion(self, newLinks)
                
        self.url=self.url.strip()+str(latestMajorVer).strip()+'/'
        
        data=Upstream.getPageData(self, self.url)
        
        if data==None:
            return latestMajorVer
            
        links=Upstream.getPageLinks(self, data)
        
        if links==None:
            print 'Unable to find links on page'
            return None
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            print 'Unable to extract version string'
            return None
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            print 'Unable to obtain latest version'
            return None
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        if latestVer==None:
            return latestMajorVer
        else:
            return latestVer