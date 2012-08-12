'''
Created on Aug 2, 2012

@author: Prashanth
'''

import urllib2
import urllib
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
        except urllib2.URLError, e:
            print 'URL Error - '+str(e.reason)
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
                
                branch=str(branch).strip()
                error=str(error).strip()
                errorMessage=str(errorMessage).strip()
                id=str(id).strip()
                url=str(url).strip()
                method=str(method).strip()
                pkgName=str(pkgName).strip()
                processed=str(processed).strip()
                
                recordList.append({'branch':branch, 'error':error, 'errorMsg':errorMessage, 'id':id, 'url':url, 'method':method, 'pkgname':pkgName, 'processed':processed})
                
            return recordList
        
    def updateRecord(self, param, value, id):
        
        if value==None:
            value='N/A'
        
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        valueString=''
        if type(value) is list:
            if len(value)==1:
                valueString=value[0]
            elif len(value)>1:
                for val in value:
                    valueString+=val+' ,'
                valueString=valueString[:-1]
            else:
                valueString='-'
        else:
            valueString=value
            
        putData='record['+param+']='+valueString
        request = urllib2.Request(self.url+':'+self.port+'/records/'+id+'.xml', data=putData)
        request.get_method = lambda: 'PUT'
        url = opener.open(request)