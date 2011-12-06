#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

print "Content-type: text/html"
print

print """
<html>

<head><title>Sample CGI Script</title></head>

<body>

  <h3> Sample CGI Script </h3>
"""

form = cgi.FieldStorage()
message = form.getvalue("upload_file", "(no file uploaded")

print """

  <p>Previous message: %s</p>

  <p>form

  <form method="post" action="submit.py">
    <p>message: <input type="file" name="upload_file"/></p>
    <p><input type="submit" name="submit_files"></p>
  </form>

</body>

</html>
""" % len(cgi.escape(message))
