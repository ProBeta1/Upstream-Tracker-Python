'''
Created on Jun 24, 2012

@author: N.B
'''

class Record(object):
    '''
    classdocs
    '''


    def __init__(self, filename):
        '''
        Constructor
        '''
        self.filename=filename
        
    def getRecords(self):
        
        records=[]
        
        f=open(self.filename)
        data=f.readlines()
        f.close()
        
        for line in data:
            line=str(line)
            pkgname=line.split(':')[0]
            method=line.split(':')[1]
            url=line[len(pkgname)+len(method)+2:]
            
            records.append([pkgname, method, url])
            
        return records
            