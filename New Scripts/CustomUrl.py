#!/usr/bin/env python

from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
import urllib2
import re

def getLatestVersion(versions):

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
	return versions[sums.index(max(sums))]

def cleanLinks(links, regex):
	newLinks=[]
	for link in links:
		try:
			m=re.compile(regex).search(link).group(0)
			newLinks.append(link[0:-1])
		except:
			m=None
	return getLatestVersion(newLinks)

def parseRegex(path, regex):
	links=[]

	data=urllib2.urlopen(path).read()
	soup=BeautifulSoup(data)
	soup.prettify()
	for link in soup.findAll('a'):
		links.append(link['href'])
	latestVer=cleanLinks(links, regex)
	return latestVer

if __name__=='__main__':

	sampleUrl='http://pan.rebelbase.com/download/releases/((\d\.*)+)/source/pan-((\d\.*)+).tar.bz2'
	parsedUrl=urlparse(sampleUrl)

	downloadPath=parsedUrl.scheme + '://' + parsedUrl.netloc

	for folder in parsedUrl.path[1:].split('/'):
		if folder.find('(')>=0 or folder.find(')')>=0:
			#print 'Working on ' + downloadPath + ' for ' + folder
			try:
				latestVer=parseRegex(downloadPath, folder)
				downloadPath=downloadPath+'/'+latestVer
			except:
				print 'unable to parse Regex'
				downloadPath=None
				break
		else:
			downloadPath=downloadPath+'/'+folder

	if downloadPath:
		print downloadPath


