'''
Created on Jun 24, 2012

@author: N.B
'''

import urllib2
from urllib2 import HTTPError, URLError
import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import re
from difflib import Match

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
        
        sums=[]

        for x in versions:
            k=10**4#len(x.split('.'))
            sum=0
            
            try:
                for m in x.split('.'):
                    sum=sum+int(m)*k/10
                    k=k/10
                sums.append(sum)
            except:
                sums.append(0)
        
        #print max(sums)
        
        return versions[sums.index(max(sums))]
    
class HTTPLS(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url=url
        
    def process(self, debugBool):
        
        error=False
        errorMsg=None
        latestVer=None
        path=None        
        
        debug=debugBool
    
        data=Upstream.getPageData(self, self.url)
        
        if data==None:
            error=True
            errorMsg='Unable to read page source'
            return (latestVer, path, error, errorMsg)
            
        links=Upstream.getPageLinks(self, data)
        
        if links==None:
            error=True
            errorMsg='Unable to find links on page'
            return (latestVer, path, error, errorMsg)
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            return (latestVer, path, error, errorMsg)
        
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            error=True
            errorMsg='Unable to extract version string'
            return (latestVer, path, error, errorMsg)
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            return (latestVer, path, error, errorMsg)
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            error=True
            errorMsg='Unable to obtain latest version'
            return (latestVer, path, error, errorMsg)
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            return (latestVer, path, error, errorMsg)
        
        fileName='Not Found'
            
        for link in links:
            if link.find(latestVer)>=0:
                fileName=link
                
        path=self.url.strip()+fileName.strip()
        
        return (latestVer, path, error, errorMsg)
    
class DualHTTPLS(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url1=url.split('|')[0]
        self.url2=url.split('|')[1]
        
    def process(self, debugBool):
        
        error=False
        errorMsg=None
        latestVer=None
        path=None
        
        debug=debugBool
        
        data1=Upstream.getPageData(self, self.url1)
        
        data2=Upstream.getPageData(self, self.url2)
        
        data=data1+data2
        
        if data1==None and data2==None:
            error=True
            errorMsg='Unable to read page source'
            return (latestVer, path, error, errorMsg)
            
        links=Upstream.getPageLinks(self, data)
        
        if links==None:
            error=True
            errorMsg='Unable to find links on page'
            return (latestVer, path, error, errorMsg)
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            error=True
            errorMsg='Unable to extract version string'
            return (latestVer, path, error, errorMsg)
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            error=True
            errorMsg='Unable to obtain latest version'
            return (latestVer, path, error, errorMsg)
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        return (latestVer, path, error, errorMsg)
    
class Launchpad(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url=url
        
    def process(self, debugBool):
        
        error=False
        errorMsg=None
        latestVer=None
        path=None
        
        debug=debugBool
        
        self.url='http://launchpad.net/'+self.url.strip()+'/+download'
        
        data=Upstream.getPageData(self, self.url)
        
        if data==None:
            error=True
            errorMsg='Unable to read page source'
            return (latestVer, path, error, errorMsg)
            
        links=Upstream.getPageLinks(self, data)
        
        if links==None:
            error=True
            errorMsg='Unable to find links on page'
            return (latestVer, path, error, errorMsg)
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            error=True
            errorMsg='Unable to extract version string'
            return (latestVer, path, error, errorMsg)
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            error=True
            errorMsg='Unable to obtain latest version'
            return (latestVer, path, error, errorMsg)
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
        
        return (latestVer, path, error, errorMsg)
    
class SVNLS(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url=url
        
    def process(self, debugBool):
        
        error=False
        errorMsg=None
        latestVer=None
        path=None
        
        debug=debugBool
    
        data=Upstream.getPageData(self, self.url)
        
        if data==None:
            error=True
            errorMsg='Unable to read page source'
            return (latestVer, path, error, errorMsg)
            
        links=Upstream.getPageLinks(self, data, 'file')
        
        if links==None:
            error=True
            errorMsg='Unable to find links on page'
            return (latestVer, path, error, errorMsg)
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            error=True
            errorMsg='Unable to extract version string'
            return (latestVer, path, error, errorMsg)
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            error=True
            errorMsg='Unable to obtain latest version'
            return (latestVer, path, error, errorMsg)
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        return (latestVer, path, error, errorMsg)

class Google(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url=url
        
    def process(self, debugBool):
        
        error=False
        errorMsg=None
        latestVer=None
        path=None
        
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
            error=True
            errorMsg='Unable to read page source'
            return (latestVer, path, error, errorMsg)
            
        links=Upstream.getPageLinks(self, data)
        
        if links==None:
            error=True
            errorMsg='Unable to find links on page'
            return (latestVer, path, error, errorMsg)
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, tarball)
        
        if versions==None:
            error=True
            errorMsg='Unable to extract version string'
            return (latestVer, path, error, errorMsg)
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            error=True
            errorMsg='Unable to obtain latest version'
            return (latestVer, path, error, errorMsg)
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        return (latestVer, path, error, errorMsg)

import ftplib
import urlparse

class FTPLS(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname.strip()
        self.url=url.strip()
        
    def process(self, debugBool):
        
        error=False
        errorMsg=None
        latestVer=None
        path=None
        
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
            error=True
            errorMsg='Unable to read page source'
            return (latestVer, path, error, errorMsg)
        
        versions=Upstream.getPageVersions(self, files, self.pkgname)
        
        if versions==None:
            error=True
            errorMsg='Unable to extract version string'
            return (latestVer, path, error, errorMsg)
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            error=True
            errorMsg='Unable to obtain latest version'
            return (latestVer, path, error, errorMsg)
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        return (latestVer, path, error, errorMsg)

class Trac(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url=url
        
    def process(self, debugBool):
        
        error=False
        errorMsg=None
        latestVer=None
        path=None
        
        debug=debugBool
    
        data=Upstream.getPageData(self, self.url)
        
        if data==None:
            error=True
            errorMsg='Unable to read page source'
            return (latestVer, path, error, errorMsg)
            
        links=Upstream.getPageLinks(self, data,'a', True)
        
        if links==None:
            error=True
            errorMsg='Unable to find links on page'
            return (latestVer, path, error, errorMsg)
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            error=True
            errorMsg='Unable to extract version string'
            return (latestVer, path, error, errorMsg)
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            error=True
            errorMsg='Unable to obtain latest version'
            return (latestVer, path, error, errorMsg)
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        return (latestVer, path, error, errorMsg)
    
class SubdirHTTPLS(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
        self.url=url
        
    def process(self, debugBool):
        
        error=False
        errorMsg=None
        latestVer=None
        path=None
        
        debug=debugBool
    
        data=Upstream.getPageData(self, self.url)
        
        if data==None:
            error=True
            errorMsg='Unable to read page source'
            return (latestVer, path, error, errorMsg)
            
        links=Upstream.getPageLinks(self, data)
        
        if links==None:
            error=True
            errorMsg='Unable to find links on page'
            return (latestVer, path, error, errorMsg)
            
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
            error=True
            errorMsg='Unable to find links on page'
            return (latestVer, path, error, errorMsg)
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            print links
            
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            error=True
            errorMsg='Unable to extract version string'
            return (latestVer, path, error, errorMsg)
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            print versions
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            error=True
            errorMsg='Unable to obtain latest version'
            return (latestVer, path, error, errorMsg)
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            print latestVer
            
        if latestVer==None:
            return (latestMajorVer, path, error, errorMsg)
        else:
            return (latestVer, path, error, errorMsg)

class SF(Upstream):
    
    def __init__(self, pkgname, url):
        Upstream.__init__(self)
        self.pkgname=pkgname
	if url.find('|')>=0:
		self.url='http://sourceforge.net/api/file/index/project-id/'+url.split('|')[0].strip()+'/rss'
	else:
        	self.url='http://sourceforge.net/api/file/index/project-id/'+url.strip()+'/rss'
	print self.url

    def process(self, debugBool):
        
        error=False
        errorMsg=None
        latestVer=None
        path=None        
        
        debug=debugBool
    
        data=Upstream.getPageData(self, self.url)

        if data==None:
            error=True
            errorMsg='Unable to read page source'
            return (latestVer, path, error, errorMsg)
        
	links=[]    
        soup=BeautifulStoneSoup(data)
	soup.prettify()
	for x in soup.findAll('link'):
	    if x.contents[0].find('/download')>=0:
		links.append(x.contents[0].split('/')[-2])
        
        if links==None:
            error=True
            errorMsg='Unable to find links on page'
            return (latestVer, path, error, errorMsg)
            
        if debug:
            print 'Links (' + self.pkgname + '): ',
            return (latestVer, path, error, errorMsg)
        
        versions=Upstream.getPageVersions(self, links, self.pkgname)
        
        if versions==None:
            error=True
            errorMsg='Unable to extract version string'
            return (latestVer, path, error, errorMsg)
        
        if debug:
            print 'Versions (' + self.pkgname + '): ',
            return (latestVer, path, error, errorMsg)
            
        latestVer=Upstream.getLatestVersion(self, versions)
        
        if latestVer==None:
            error=True
            errorMsg='Unable to obtain latest version'
            return (latestVer, path, error, errorMsg)
#        else:
#            print 'Latest Version (' + self.pkgname + '): ' + str(latestVer)
        
        if debug:
            print 'Latest Version (' + self.pkgname + '): ',
            return (latestVer, path, error, errorMsg)
        
        fileName='Not Found'
            
        for link in links:
            if link.find(latestVer)>=0:
                fileName=link
                
        path=self.url.strip()+fileName.strip()
        
        return (latestVer, path, error, errorMsg)

