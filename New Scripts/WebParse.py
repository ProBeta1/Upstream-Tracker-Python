'''
Created on Jul 2, 2012

@author: N.B
'''

import urllib2
from xml.dom.minidom import parse, parseString
 
class WebParse(object):
    '''
    classdocs
    '''


    def __init__(self, url, port):
        '''
        Constructor
        '''
        self.url=url
        self.port=port
        
    def getRecords(self):
        try:
            data=urllib2.urlopen(self.url+':'+self.port+'/records.xml').read()            
#        except HTTPError, e:
#            print 'HTTP Error - '+e.reason
#            return None
        except URLError, e:
            print 'URL Error - '+e.reason
            data=None
            return None
        
        if data:
            dom=parseString(data)
            records=dom.getElementsByTagName('record')
            
            recordList=[]
            
            for record in records:
                branch=record.getElementsByTagName('branch')[0].firstChild.data
                error=record.getElementsByTagName('error')[0].firstChild.data
                if str(error)=='True':
                    errorMessage=record.getElementsByTagName('errorMessage')[0].firstChild.data
                else:
                    errorMessage=''
                id=record.getElementsByTagName('id')[0].firstChild.data
                url=record.getElementsByTagName('info')[0].firstChild.data
                method=record.getElementsByTagName('method')[0].firstChild.data
                pkgName=record.getElementsByTagName('pkgName')[0].firstChild.data
                processed=record.getElementsByTagName('processed')[0].firstChild.data
                
                recordList.append({'branch':branch, 'error':error, 'errorMsg':errorMessage, 'id':id, 'url':url, 'method':method, 'pkgname':pkgName, 'processed':processed})
                
            return recordList
        
    def updateRecord(self, param, value, id):
        
        if value==None:
            value='N/A'
        
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        putData='record['+param+']='+value
        request = urllib2.Request(self.url+':'+self.port+'/records/'+id+'.xml', data=putData)
        request.get_method = lambda: 'PUT'
        url = opener.open(request)