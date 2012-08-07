'''
Created on Aug 2, 2012

@author: Prashanth
'''

import threading, Queue
import sys
from WebParse import WebParse
from Upstream import Upstream, HTTPLS, FTPLS, Google, Launchpad, SVNLS, Trac,\
    SubdirHTTPLS, DualHTTPLS, Custom 

THREAD_LIMIT = 5             
jobs = Queue.Queue(50)          
singlelock = threading.Lock()   
 
inputlist_ori = []

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
    processed=record['processed']
    
    inputlist_ori.append([pkgname, method, url, id, processed])
    
def main(inputlist):
    print "Inputlist received..."
    print inputlist
 
    print "Spawning the {0} threads.".format(THREAD_LIMIT)
    for x in xrange(THREAD_LIMIT):
        print "Thread {0} started.".format(x)
        workerbee().start()
 
    print "Putting stuff in queue"
    for i in inputlist:
        try:
            jobs.put(i, block=True, timeout=5)
        except:
            singlelock.acquire()
            print "The queue is full !"
            singlelock.release()
 
    singlelock.acquire()
    print "Waiting for threads to finish."
    singlelock.release()
    jobs.join()         

class workerbee(threading.Thread):
    
    def process(self, pkgname, method, url, id):
        
        wp = WebParse('http://localhost','3000')
        
        errorMsg=''
            
        if method=='httpls':
            upstream=HTTPLS(url, pkgname)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='dualhttpls':
            upstream=DualHTTPLS(url, pkgname)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='lp':
            upstream=Launchpad(url, pkgname)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='svnls':
            upstream=SVNLS(url, pkgname)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='google':
            upstream=Google(url, pkgname)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='ftpls':
            upstream=FTPLS(url, pkgname)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='trac':
            upstream=Trac(url, pkgname)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='sf':
            upstream=SF(url, pkgname)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='custom':
            custom=Custom(url, pkgname)
            (ver,loc,error) = custom.process()
            print pkgname, ver, loc
            
        if error==None:
            error=False
            errorMsg='None'
        else:
            errorMsg=error
            error=True
            
            
        wp.updateRecord('error', str(error).lower(), id)
        wp.updateRecord('errorMessage', errorMsg, id)
        wp.updateRecord('processed', 'true', id)
        wp.updateRecord('latest_ver', ver, id)
        wp.updateRecord('loc', loc, id)
    
    def run(self):
        while 1:
            try:
                job = jobs.get(True,1)
                self.process(job[0],job[1],job[2],job[3])
                jobs.task_done()
            except:
                break

if __name__ == '__main__':
    main(inputlist_ori)    
