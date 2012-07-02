'''
Created on Jul 2, 2012

@author: N.B
'''

# Test module to handle custom urls with regex

a='http://pan.rebelbase.com/download/releases/(.*)/source/pan-(.*).tar.bz2'
b=a.split('://')[1].split('/')
m=''

import urllib2
import BeautifulSoup

for x in b:
    if x.find('(')>=0:
        prefix=None
        suffix=None
#        print m
        
        if(len(x[:x.find('(')])>0):
            prefix=x[:x.find('(')]
        
        if(len(x[x.find(')'):])>1):
            suffix=x[x.find(')')+1:]
        
#        print prefix, suffix
        
        data=urllib2.urlopen('http:/'+m).read()
        soup=BeautifulSoup.BeautifulSoup(data)
        soup.prettify()
        links=[]
        for link in soup.findAll('a'):
            href=str(link['href'])
            if prefix or suffix:
                if href.find(prefix)==0 or href.find(suffix)==len(href)-len(suffix):
                    links.append(href)
            else:
                if href[0].isdigit():
                    links.append(href[:len(href)-1]) 
                                 
        print links
        
        upstream=Upstream.Upstream()
        m=m+'/'+upstream.getLatestVersion(links)[:len(upstream.getLatestVersion(links))]
    else:
        m=m+'/'+x
