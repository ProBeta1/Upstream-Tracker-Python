#!/bin/python

import pycurl
import cStringIO
import urllib

data = {'record[pkgName]':'pycurl test 1', 'record[branch]':'testing', 'record[method]':'http', 'record[info]':'http://sample.com'  }

post = urllib.urlencode(data)

buf = cStringIO.StringIO()
 
c = pycurl.Curl()
c.setopt(c.CUSTOMREQUEST, "PUT")
c.setopt(c.URL, 'http://localhost:3000/records/11.xml')
c.setopt(c.POSTFIELDS, post)
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()
 
print buf.getvalue()
buf.close()