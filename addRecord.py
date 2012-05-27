#!/bin/python

import pycurl
import cStringIO
import urllib

data = {'record[pkgName]':'pycurl test', 'record[branch]':'testing', 'record[method]':'http', 'record[info]':'http://sample.com'  }

post = urllib.urlencode(data)

buf = cStringIO.StringIO()
 
c = pycurl.Curl()
c.setopt(c.URL, 'http://localhost:3000/records.xml')
c.setopt(c.POST, 1)
c.setopt(c.POSTFIELDS, post)
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()
 
print buf.getvalue()
buf.close()