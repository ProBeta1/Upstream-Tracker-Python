'''
Created on 25-Jul-2012

@author: nbprashanth
'''

from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
import urllib2
import re

class CustomURL:
    def getPageVersions(self, links):
        versions=[]
        for link in links:
            if link[0].isdigit():
                versions.append(link)
            else:
                try:
                    m=re.compile('^.*[-_]((\d\.*)+).*').match(link).group(1)
                    versions.append(m[0:-1])
                except:
                    pass

        if len(versions)==0:
            return None
        else:
            return versions 

    def getLatestVersion(self,versionsOld):
        versions=self.getPageVersions(versionsOld)
        sums=[]
        for x in versions:
            k=10**5#len(x.split('.'))
            sum=0
            try:
                for m in x.split('.'):
                    sum=sum+int(m)*k/10
                    k=k/10
                sums.append(sum)
            except:
                sums.append(0)

        maxVer=versions[sums.index(max(sums))]

        for x in versionsOld:
            if x.find(maxVer)>=0:
                return x

    def cleanLinks(self, links, regex):
        newLinks=[]

        for link in links:
            try:
                m=re.compile(regex).search(link).group(0)
                if link.find('/')>=0:
                    newLinks.append(link[0:-1])
                else:
                    newLinks.append(link)
            except:
                m=None

        return self.getLatestVersion(newLinks)

    def parseRegex(self, path, regex):
        links=[]

        data=urllib2.urlopen(path).read()
        soup=BeautifulSoup(data)
        soup.prettify()
        for link in soup.findAll('a'):
            links.append(link['href'])

        latestVer=self.cleanLinks(links, regex)
        return latestVer

    def process(self, Url):
 
    #    sampleUrl='http://pan.rebelbase.com/download/releases/((\d\.*)+)/source/pan-((\d\.*)+).tar.bz2'
    #    sampleUrl='http://www.freedesktop.org/software/ConsoleKit/dist/ConsoleKit-((\d\.*)+).tar.(.*)'
        parsedUrl=urlparse(Url)

        downloadPath=parsedUrl.scheme + '://' + parsedUrl.netloc

        for folder in parsedUrl.path[1:].split('/'):
            if folder.find('(')>=0 or folder.find(')')>=0:
                #print 'Working on ' + downloadPath + ' for ' + folder
                try:
                    latestVer=self.parseRegex(downloadPath, folder)
                    downloadPath=downloadPath+'/'+latestVer
                except:
                    #print 'unable to parse Regex'
                    downloadPath=None
                    break
            else:
                downloadPath=downloadPath+'/'+folder

        if downloadPath:
            return re.compile('^.*[-_]((\d\.*)+).*').match(latestVer).group(1)[0:-1], downloadPath
        else:
            return None, None
