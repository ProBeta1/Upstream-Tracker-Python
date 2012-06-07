#!/usr/bin/env python2


import pycurl
import cStringIO
 
buf = cStringIO.StringIO()
 
c = pycurl.Curl()
c.setopt(c.URL, 'http://localhost:3000/records.xml')
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()
 
print buf.getvalue()
buf.close()