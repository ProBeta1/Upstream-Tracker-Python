'''
Created on Aug 2, 2012

@author: Prashanth
'''

import urllib2
import ftplib
import re
import Util
import xml.dom.minidom as minidom
    
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup


class Upstream(object):
    '''
    classdocs
    '''
    
    def checkValidExt(self, link):
        validExt=['gz', 'bz2']
        
        for ext in validExt:
            if link.split('.')[-1]==ext:
                return True
            
        return False                                       

    def getPageLinks(self, url):
        
        parsedUrl=urlparse(url)
        
        scheme=parsedUrl.scheme
        hostname=parsedUrl.hostname
        path=parsedUrl.path
        
        error=None
        links=[]
        
        if scheme=='http' or scheme=='https':
            try:
                data=urllib2.urlopen(url).read()
            except Exception, e:
                error='Unable to open URL'
                return None, error
            
            soup=BeautifulSoup(data)
            soup.prettify()
            
            try:
                for link in soup.findAll('a')+soup.findAll('file'):
                    if self.checkValidExt(link['href']):
                        links.append(scheme+'://'+hostname+path+link['href'])
            except:
                try:
                    for link in soup.findAll('a'):
                        if self.checkValidExt(link['href']):
                            links.append(scheme+'://'+hostname+path+str(link.contents).replace('\n','').strip())
                except:
                    pass
            
            if len(links)>0:
                return links, error
            else:
                error='No links found'
                return None, error
        
        if scheme=='ftp':
            
            files = []
            
            try:
                ftp = ftplib.FTP(hostname)
                ftp.login("anonymous", "")
                ftp.cwd(path)
            except Exception, e:
                error='Unable to open URL'
                return None, error
            
            try:
                files = ftp.nlst()
                for file in files:
                    if self.checkValidExt(file):
                        links.append(scheme+'://'+hostname+'/'+file)
            except ftplib.error_perm, resp:
                if str(resp) == "550 No files found":
                    print "No files in this directory"
                else:
                    raise
            return links, error
    
    def getVersions(self, links, regex):
        
        newLinks=[]
        error=None
        
        for link in links:
            try:
                match=re.match(regex, link)
                if match.group(0).find('/')>=0:
                    newLinks.append(match.group(1).split('/')[-1])
                else:                
                    newLinks.append(match.group(1))
            except Exception, e:
                pass
            
        if len(newLinks)==0:
            error='Unable to process links'
            return None, error
        else:
            return newLinks, error
        
    def getLatestVersion(self, versions, branch):
        
        latestVerList=[]
        
        util=Util.Util()
#        latestVer=versions[0].replace('-','.').replace('_','.')
#        
#        for version in versions:
#            if util.version_gt(version.replace('-','.').replace('_','.'), latestVer):
#                latestVer=version
#        latestVerList.append(latestVer)       
#        
#        for x in range(0,int(latestVer.split('.')[0]+latestVer.split('.')[1])):
#            latestVer='0.0'
#            for version in versions:
#                if int(version.replace('-','.').replace('_','.').split('.')[0])==x:
#                    if util.version_gt(version.replace('-','.').replace('_','.'), latestVer):
#                        latestVer=version
#            if latestVer!='0.0':
#                latestVerList.append(latestVer)

        if branch=='latest':
            latestVer=versions[0]
            for version in versions:
                cleanVer=util.cleanVerStr(version)
                if util.version_gt(cleanVer, util.cleanVerStr(latestVer)):
                    latestVer=version                    
            latestVerList.append(latestVer)
        else:
            for eachBranch in branch.split(','):
                latestVer=util.cleanVerStr(versions[0])
                for version in versions:
                    br=eachBranch.strip().replace('.','\.')
                    br=br+'.*'
                    x=re.match(br, version)
                    if x:
                        cleanVer=util.cleanVerStr(version)
                        if util.version_gt(cleanVer, latestVer):
                            latestVer=version
                latestVerList.append(latestVer)        
        
        if len(latestVer)>0:
            return latestVerList, None
        else:
            return None, 'Unable to find Latest Version'
    
    def getLocation(self, links, latestVer):
        
        locs=[]
        for ver in latestVer:
            for link in links:
                if link.replace('-','.').replace('_','.').find(ver)>=0:
                    locs.append(link)
                    
        if len(locs)>0:
            return locs, None
        else:
            return None, 'Unable to find Location'
    
class HTTPLS(Upstream):
    
    def __init__(self, url, pkgname, branch):
        
        self.url=url
        self.pkgname=pkgname
        self.branch=branch
        
    def process(self):
        
        (links, error)=self.getPageLinks(self.url)
        if error:
            return None, None, error
        (versions, error)=self.getVersions(links, '^.*'+self.pkgname+'[_-](([0-9]+[\.\-])*[0-9]+)\.(?:tar.*|t[bg]z2?).*$')
        if error:
            return None, None, error
        (latestVer, error) = self.getLatestVersion(versions, self.branch)
        if error:
            return None, None, error
        (location, error) = self.getLocation(links, latestVer)
        return latestVer, location, None
    
class DualHTTPLS(Upstream):
    
    def __init__(self, url, pkgname, branch):
        
        self.url1=url.split('|')[0]
        self.url2=url.split('|')[1]
        self.pkgname=pkgname
        self.branch=branch
        
    def process(self):
        
        (links1, error)=self.getPageLinks(self.url1)
        if error:
            return None, None, error
        (links2, error)=self.getPageLinks(self.url1)
        if error:
            return None, None, error
        links=links1+links2
        (versions, error)=self.getVersions(links, '^.*'+self.pkgname+'[_-](([0-9]+[\.\-])*[0-9]+)\.(?:tar.*|t[bg]z2?).*$')
        if error:
            return None, None, error
        (latestVer, error) = self.getLatestVersion(versions, self.branch)
        if error:
            return None, None, error
        (location, error) = self.getLocation(links, latestVer)
        return latestVer, location, None
    
class FTPLS(Upstream):
    
    def __init__(self, url, pkgname, branch):
        
        self.url=url
        self.pkgname=pkgname
        self.branch=branch
        
    def process(self):
        
        (links, error)=self.getPageLinks(self.url)
        if error:
            return None, None, error
        (versions, error)=self.getVersions(links, '^.*'+self.pkgname+'[_-](([0-9]+[\.\-])*[0-9]+)\.(?:tar.*|t[bg]z2?).*$')
        if error:
            return None, None, error
        (latestVer, error) = self.getLatestVersion(versions, self.branch)
        if error:
            return None, None, error
        (location, error) = self.getLocation(links, latestVer)
        return latestVer, location, None
    
class Google(Upstream):
    
    def __init__(self, url, pkgname, branch):
        
        self.url='http://code.google.com/p/'+url.strip()+'/downloads/list'
        self.pkgname=pkgname
        self.branch=branch
        
    def process(self):
        
        (links, error)=self.getPageLinks(self.url)
        if error:
            return None, None, error
        (versions, error)=self.getVersions(links, '^.*'+self.pkgname+'[_-](([0-9]+[\.\-])*[0-9]+)\.(?:tar.*|t[bg]z2?).*$')
        if error:
            return None, None, error
        (latestVer, error) = self.getLatestVersion(versions, self.branch)
        if error:
            return None, None, error
        (location, error) = self.getLocation(links, latestVer)
        newLoc=[]
        for loc in location:
            newLoc.append(urlparse(self.url).scheme+'://'+loc.split('//')[2])
            
        return latestVer, newLoc, None
    
class Launchpad(Upstream):

    def __init__(self, url, pkgname, branch):
        
        self.url='http://launchpad.net/'+url.strip()+'/+download'
        self.pkgname=pkgname
        self.branch=branch
        
    def process(self):
        
        (links, error)=self.getPageLinks(self.url)
        if error:
            return None, None, error
        (versions, error)=self.getVersions(links, '^.*'+self.pkgname+'[_-](([0-9]+[\.\-])*[0-9]+)\.(?:tar.*|t[bg]z2?).*$')
        if error:
            return None, None, error
        (latestVer, error) = self.getLatestVersion(versions, self.branch)
        if error:
            return None, None, error
        (location, error) = self.getLocation(links, latestVer)
        newLoc=[]
        for loc in location:
            newLoc.append(loc.replace('http://launchpad.net/dee/+download',''))
        return latestVer, newLoc, None
    
class SVNLS(Upstream):
    
    def __init__(self, url, pkgname, branch):
        
        self.url=url
        self.pkgname=pkgname
        self.branch=branch
        
    def process(self):
        
        (links, error)=self.getPageLinks(self.url)
        if error:
            return None, None, error
        (versions, error)=self.getVersions(links, '^.*'+self.pkgname+'[_-](([0-9]+[\.\-])*[0-9]+)\.(?:tar.*|t[bg]z2?).*$')
        if error:
            return None, None, error
        (latestVer, error) = self.getLatestVersion(versions, self.branch)
        if error:
            return None, None, error
        (location, error) = self.getLocation(links, latestVer)
        return latestVer, location, None
    
class Trac(Upstream):
    
    def __init__(self, url, pkgname, branch):
        
        self.url=url
        self.pkgname=pkgname
        self.branch=branch
        
    def process(self):
        
        (links, error)=self.getPageLinks(self.url)
        if error:
            return None, None, error
        (versions, error)=self.getVersions(links, '^.*'+self.pkgname+'[_-](([0-9]+[\.\-])*[0-9]+)\.(?:tar.*|t[bg]z2?).*$')
        if error:
            return None, None, error
        (latestVer, error) = self.getLatestVersion(versions, self.branch)
        if error:
            return None, None, error
        (location, error) = self.getLocation(links, latestVer)
        return latestVer, location, None
    
class SubdirHTTPLS(Upstream):
    
    def __init__(self, url, pkgname, branch):
        
        self.url=url
        self.pkgname=pkgname
        self.branch=branch
        
    def process(self):
        
        flag=0
        
        (links, error)=self.getPageLinks(self.url)
        if error:
            return None, None, error
            
        while True:
            
            (versions, error)=self.getVersions(links, '^.*/([\d\.]+)/')
            if error:
                return None, None, error
            (latestVer, error) = self.getLatestVersion(versions[0], self.branch)
            
            self.url=self.url+latestVer+'/'
            
            (links, error)=self.getPageLinks(self.url)
            if error:
                return None, None, error
            
            for link in links:
                if link.find(self.pkgname)>=0 and link.find('.tar')>=0:
                    flag=1
                    break            
                
            if flag==1:
                break
            
        (versions, error)=self.getVersions(links, '^.*'+self.pkgname+'[_-](([0-9]+[\.\-])*[0-9]+)\.(?:tar.*|t[bg]z2?).*$')
        if error:
            return None, None, error
        (latestVer, error) = self.getLatestVersion(versions)
        if error:
            return None, None, error
        (location, error) = self.getLocation(links, latestVer)
        return latestVer, location, None
    
class Custom(Upstream):
    
    def __init__(self, url, pkgname, branch):
        
        self.url=url
        self.pkgname=pkgname
        self.branch=branch
        
    def parseRegex(self, path, regex):
        
        (links, error)=self.getPageLinks(path)
        if error:
            return None, None, error
        
        (versions, error)=self.getVersions(links, '^.*/'+regex)
        if error:
            return None, None, error
        
#        newVersions=[]
#        for version in versions:
#            m=re.sub('-','',re.sub('[a-zA-Z-_]', '', version))
#            m=m.replace('..','.')
#            newVersions.append(m)

        newVersions=versions
                                
        (latestVer, error) = self.getLatestVersion(newVersions, self.branch)
        if error:
            return None, None, error
        
        (location, error) = self.getLocation(links, latestVer)
        return latestVer, location, None
    
    def processSf(self):
        regex=self.url.split('/')[-1]
        doc = minidom.parseString(urllib2.urlopen('/'.join(self.url.split('/')[:-1])).read())
        items = doc.getElementsByTagName('item')
        
        links=[]
        for item in items:
            linkObj=item.getElementsByTagName('link')[0]
            nodes = linkObj.childNodes
            for node in nodes:
                if node.nodeType == node.TEXT_NODE:
                    try:
                        link=node.data.replace('/download','')
                        match=re.match('^.*/'+regex, link)
                        links.append(match.group(0))            
                    except Exception, e:
                        pass
                    
        (versions, error)=self.getVersions(links, '^.*/'+regex)
        if error:
            return None, None, error
        
        newVersions=[]
        for version in versions:
            m=re.sub('-','',re.sub('[a-zA-Z-_]', '', version))
            m=m.replace('..','.')
            newVersions.append(m)

        (latestVer, error) = self.getLatestVersion(newVersions, self.branch)
        if error:
            return None, None, error
        
        (location, error) = self.getLocation(links, latestVer)
        if error:
            return None, None, error
        
        return latestVer[0], location, None
        
    def process(self):
        
        parsedUrl=urlparse(str(self.url))
        downloadDir=parsedUrl.scheme+'://'+parsedUrl.hostname
        
        if parsedUrl.hostname.find('sf.net')>=0 or parsedUrl.hostname.find('sourceforge.net')>=0:
            return self.processSf()
            
        for dir in parsedUrl.path.split('/'):
            if dir.find('(')>=0 or dir.find(')')>=0:
                
                if parsedUrl.hostname=='code.google.com':
                    if downloadDir[-1]=='/':
                        downloadDir=downloadDir[:-1]
                        
                (latestVer, loc, error)=self.parseRegex(downloadDir, dir)
                
                if loc!=None and loc.find('/')>=0: 
                    if downloadDir[-1]=='/':
                        downloadDir+=loc.split('/')[-1]
                    else:
                        downloadDir+='/'+loc.split('/')[-1]
                else:
                    downloadDir+=latestVer[0]+'/'
            else:
                downloadDir+=dir+'/'
        
        return latestVer, downloadDir, error