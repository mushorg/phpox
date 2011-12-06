#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()
import sys
import os
import hashlib
sandbox_path = "../../"

sandbox_path_abs = "/home/guesslin/workspace/phpsandbox/php_sandbox-git/trunk/"
sys.path.append(sandbox_path_abs)
import apd_sandbox

print "Context-type: text/html"
print
print """
<html>
<head><title>Test upload pages</title></head>
<body>
"""

form = cgi.FieldStorage()
if not form:
    print """
    <form action="submit.py" method="POST" enctype="multipart/form-data">
    <input type="file" name="filename" />
    <input type="submit" name="submit" />
    </form>
    """
elif form.has_key("filename"):
    item = form["filename"]
    if item.file:
        data = item.file.read()
        print data
        sample_name = hashlib.md5(data).hexdigest()
        fout = file(os.path.join(sandbox_path_abs + "samples/", sample_name), "w")
        fout.write(data)
        fout.close()
        apd_sandbox.sandbox(sandbox_path_abs + "samples/" + sample_name, 5)


print """
</body>
</html>
"""
