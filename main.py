import threading, Queue
import sys
from WebParse import WebParse
from Upstream import HTTPLS, FTPLS, Google, Launchpad, SVNLS, Trac,\
    SubdirHTTPLS, DualHTTPLS, Custom, SF
import time
from datetime import datetime, timedelta
from time import gmtime, strftime

THREAD_LIMIT = 2
QUEUE_LIMIT = 50
URL = 'http://localhost'
PORT = '3000'
THREAD_WAIT = 5 

HOURS_LIMIT=1

# On an average, no of records processed is : 1 for every THREAD_WAIT seconds

jobs = Queue.Queue(QUEUE_LIMIT)          
singlelock = threading.Lock()   

inputlist_ori = []

wp = WebParse(URL, PORT)
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
	updated=record['updated-at']

	date_object = datetime.strptime(updated, '%Y-%m-%dT%H:%M:%SZ')
        curr_dt=datetime.strptime(strftime('%Y-%m-%dT%H:%M:%SZ', gmtime()), '%Y-%m-%dT%H:%M:%SZ')

	if (processed=='true' and ((curr_dt-date_object)-timedelta(hours=HOURS_LIMIT)).seconds/3600<=0) or processed=='false':
		print 'Processing ' + pkgname + ' ; Time difference : ' + str((timedelta(hours=HOURS_LIMIT)-(curr_dt-date_object)).seconds/3600)
		inputlist_ori.append([pkgname, method, url, id, processed, branch])
	else:
		print 'Not processing ' + pkgname + ' ; Time difference : ' + str((curr_dt-date_object).seconds/3600) +'H '+str(((curr_dt-date_object).seconds-3600)/60) +'M'

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
        
        wp = WebParse(URL,PORT)
        
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
