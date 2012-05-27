#!/bin/python

import pycurl
import cStringIO
import urllib

buf = cStringIO.StringIO()
 
c = pycurl.Curl()
c.setopt(c.CUSTOMREQUEST, "DELETE")
c.setopt(c.URL, 'http://localhost:3000/records/11.xml')
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()
 
print buf.getvalue()
buf.close()