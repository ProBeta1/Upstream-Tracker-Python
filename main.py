import threading, Queue
import sys
from WebParse import WebParse
from Upstream import HTTPLS, FTPLS, Google, Launchpad, SVNLS, Trac,\
    SubdirHTTPLS, DualHTTPLS, Custom, SF

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
    branch=record['branch']
    
    inputlist_ori.append([pkgname, method, url, id, processed, branch])
    
def main(inputlist):
    for x in xrange(THREAD_LIMIT):
        workerbee().start()
 
    for i in inputlist:
        try:
            jobs.put(i, block=True, timeout=5)
        except:
            pass
    
    jobs.join()         

class workerbee(threading.Thread):
    
    def process(self, pkgname, method, url, id, branch):
        
        wp = WebParse('http://localhost','3000')
        
        errorMsg=''
        
        if method=='httpls':
            upstream=HTTPLS(url, pkgname, branch)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='subdirhttpls':
            upstream=SubdirHTTPLS(url, pkgname, branch)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='dualhttpls':
            upstream=DualHTTPLS(url, pkgname, branch)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='lp':
            upstream=Launchpad(url, pkgname, branch)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='svnls':
            upstream=SVNLS(url, pkgname, branch)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='google':
            upstream=Google(url, pkgname, branch)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='ftpls':
            upstream=FTPLS(url, pkgname, branch)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='trac':
            upstream=Trac(url, pkgname, branch)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='sf':
            upstream=SF(url, pkgname, branch)
            (ver,loc,error) = upstream.process()
            print pkgname, ver, loc
            
        if method=='custom':
            custom=Custom(url, pkgname, branch)
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
                self.process(job[0],job[1],job[2],job[3], job[5])
                jobs.task_done()
            except:
                break

if __name__ == '__main__':
    main(inputlist_ori)