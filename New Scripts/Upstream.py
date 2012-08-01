'''
Created on 23-Jul-2012

@author: nbprashanth
'''

from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

import urllib2
import ftplib
import re

class Upstream(object):
    '''
    classdocs
    '''
    
    def __init__(self, pkgname, url):
        '''
        Constructor
        '''
        self.url=url
        self.pkgname=pkgname
    
    def setUrl(self, url):
        self.url=url
        
    def getLinks(self, tag='a', contents=False):
        
        data=None
        parsedUrl=urlparse(self.url)
        scheme=parsedUrl.scheme
                
        if scheme=='http' or scheme=='https':
            links = []
            rawLinks = []
            
            try:
                data=urllib2.urlopen(self.url).read()
                
                soup=BeautifulSoup(data)
                soup.prettify()
                
                for link in soup.findAll(tag):
                    if contents:
                        linkText=link.contents                        
                    else:
                        linkText=link['href']
                        
                    rawLinks.append(linkText)
                    
                    if str(linkText).find(self.pkgname)>=0:
                        links.append(linkText)
                    
                return links, rawLinks
            
            except Exception, e:
                print 'An exception occured while fetching URL - ', e
                
        elif scheme=='ftp':
            files = []
            links = []
            ftp = ftplib.FTP(parsedUrl.hostname)
            ftp.login("anonymous", "")
            ftp.cwd(parsedUrl.path)
            
            try:
                files = ftp.nlst()
                for file in files:
                    if file.find(self.pkgname)>=0:
                        links.append(file)
                return links, links
            except ftplib.error_perm, resp:
                if str(resp) == "550 No files found":
                    print "No files in this directory"
                else:
                    raise
        else:
            return None, None
                
    def getLatestVer(self, links, append=True):
        
        versions=[]
        latestVer=None
        latestVerString=None
        location=None
        versionSum=0
        
        if links==None:
            return None, None
        
        for link in links:
            try:
                matchObj=re.search('^.*'+self.pkgname+'[_-](([0-9]+[\.\-])*[0-9]+)\.(?:tar.*|t[bg]z2?).*$', str(link))
                versions.append(matchObj.group(1))
            except:
                pass  
            
        for version in versions:
            k=10**4
            versionSum=0
            for digit in version.split('.'):
                versionSum=versionSum+int(digit)*k/10
                k=k/10     
            if versionSum>latestVer:
                latestVer=versionSum
                latestVerString=version
            
        for link in links:
            if str(link).find(latestVerString)>=0:
                if append:
                    if type(link) is list:
                        location=self.url+str(link[0].strip())
                    else:
                        location=self.url+str(link)
                else:
                    if type(link) is list:
                        location=str(link[0].strip())
                    else:
                        location=str(link)
                
        return latestVerString, location
    
class HTTPLS(Upstream):
    def __init__(self, pkgname, url):
        super(HTTPLS, self).__init__(pkgname, url)
    def process(self):
        (links, rawLinks)=self.getLinks()
        return self.getLatestVer(links)
    
class DualHTTPLS(object):
    def __init__(self, pkgname, url):
        self.url1=url.split('|')[0]
        self.url2=url.split('|')[1]
        self.pkgname=pkgname
    def process(self):
        upstream1=Upstream(self.pkgname, self.url1)
        upstream2=Upstream(self.pkgname, self.url2)
        (links1, rawLinks1)=upstream1.getLinks()
        (links2, rawLinks2)=upstream2.getLinks()
        latestVer1=upstream1.getLatestVer(links1)
        latestVer2=upstream2.getLatestVer(links2)
        versions=[latestVer1[0], latestVer2[0]]
        
        latestVer=None
        latestVerString=None
        
        for version in versions:
            k=10**4
            versionSum=0
            for digit in version.split('.'):
                versionSum=versionSum+int(digit)*k/10
                k=k/10     
            if versionSum>latestVer:
                latestVer=versionSum
                latestVerString=version
        
        if latestVerString==latestVer1[0]:
            location=latestVer1[1]
        else:
            location=latestVer1[1].replace(self.url1,self.url2)
            
        return latestVerString, location
    
class Launchpad(Upstream):
    def __init__(self, pkgname, url):
        url='http://launchpad.net/'+url.strip()+'/+download'
        super(Launchpad, self).__init__(pkgname, url)
    def process(self):
        (links, rawLinks)=self.getLinks()
        return self.getLatestVer(links, False)
    
class SVNLS(Upstream):
    def __init__(self, pkgname, url):
        super(SVNLS, self).__init__(pkgname, url)
    def process(self):
        (links, rawLinks)=self.getLinks('file')
        return self.getLatestVer(links)
    
class Google(Upstream):
    def __init__(self, pkgname, url):
        
        if url.find('|')>=0:
            self.tarball=url.split('|')[1].strip()
            self.prjname=url.split('|')[0].strip()
        else:
            self.tarball=url.strip()
            self.prjname=url.strip()
            
        url='http://code.google.com/p/'+self.prjname.strip()+'/downloads/list'
        
        super(Google, self).__init__(pkgname, url)
    def process(self):
        (links, rawLinks)=self.getLinks()
        return self.getLatestVer(links)
    
class FTPLS(Upstream):
    def __init__(self, pkgname, url):
        super(FTPLS, self).__init__(pkgname, url)
    def process(self):
        (links, rawLinks)=self.getLinks()
        return self.getLatestVer(links)
    
class Trac(Upstream):
    def __init__(self, pkgname, url):
        super(Trac, self).__init__(pkgname, url)
    def process(self):
        (links, rawLinks)=self.getLinks('a',True)
        return self.getLatestVer(links)
    
class SF(Upstream):
    def __init__(self, pkgname, url, name=False):
        if name:
            self.url='http://sourceforge.net/api/file/index/project-name/'+url.strip()+'/rss'            
        else:
            if url.find('|')>=0:
                self.url='http://sourceforge.net/api/file/index/project-id/'+url.split('|')[0].strip()+'/rss'
            else:
                self.url='http://sourceforge.net/api/file/index/project-id/'+url.strip()+'/rss'
        super(SF, self).__init__(pkgname, self.url)
    def process(self):
        links=[]
        data=urllib2.urlopen(self.url).read()
        soup=BeautifulStoneSoup(data)
        soup.prettify()
        for x in soup.findAll('link'):
            if x.contents[0].find('/download')>=0:
                links.append(x.contents[0].split('/')[-2])
        return self.getLatestVer(links)
    
#class SubdirHTTPLS(Upstream):
#    def __init__(self, pkgname, url):
#        self.url=url
#        super(SubdirHTTPLS, self).__init__(pkgname, url)
#    def process(self):
#        
#        url=self.url
#        files=[]
#        
#        while True:
#            self.setUrl(url)
#            
#            (links, rawLinks)=self.getLinks()
#            
#            good_dir = re.compile('^(([0-9]+|[xX])\.)*([0-9]+|[xX])/?$')
#            def hasdirs(x): return good_dir.search(x)
#            def fixdirs(x): return re.sub(r'^((?:(?:[0-9]+|[xX])\.)*)([0-9]+|[xX])/?$', r'\1\2', x)
#            
#            newdirs = filter(hasdirs, rawLinks)
#            newdirs = map(fixdirs, newdirs)
#            
#            if len(newdirs)==0:
#                url=url[:-1]
#                break
#            
#            print newdirs
#            
#            url=url+newdirs[0]+'/'
#            
#        self.setUrl(url)
#        print url
#        (links, rawLinks)=self.getLinks()
#        print links
