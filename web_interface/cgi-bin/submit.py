#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()
import sys
import os
import hashlib

sandbox_path = os.getcwd().rsplit("/", 1)[0]
sys.path.append(sandbox_path)
import apd_sandbox

def form_body():
    return """
    <form action="submit.py" method="POST" enctype="multipart/form-data">
    <input type="file" name="filename" />
    <input type="submit" name="submit" />
    <input type="radio" name="xml" value="0">HTML</input>
    <input type="radio" name="xml" value="1">XML</intput>
    </form>
    """

form = cgi.FieldStorage()

if not form:
    print "Content-type: text/html"
    print
    print """
    <html>
    <head><title>Test upload pages</title></head>
    <body>
    """ + form_body() + """
    </body>
    </html>
    """
elif form.has_key("filename"):
    item = form["filename"]
    xml = form["xml"].value
    if item.file:
        data = item.file.read()
        #print data
        sample_name = hashlib.md5(data).hexdigest()
        fout = file(os.path.join(sandbox_path + "/samples/", sample_name), "w")
        fout.write(data)
        fout.close()
        botnet = apd_sandbox.sandbox(sandbox_path + "/samples/" + sample_name, 5, pre=sandbox_path + '/')
        if(xml == "1"):
            print "Content-type: text/xml"
            print
            print botnet.toxml()
        else:
            print "Content-type: text/html"
            print
            print "<html>"
            print "<body>"
            print form_body()
            print "file md5: %s<br />" % botnet.file_md5
            print "irc_addr: %s<br />" % botnet.irc_addr
            print "irc_server_pwd: %s<br />" % botnet.irc_server_pwd
            print "irc_nick: %s<br />" % botnet.irc_nick
            print "irc_user: %s<br />" % botnet.irc_user
            print "irc_mode: %s<br />" % botnet.irc_mode
            for i in botnet.irc_channel :
                print "irc_channel: %s<br />" % i
            print "nickserv: %s<br />" % botnet.irc_nickserv
            for i in botnet.irc_notice :
                print "irc_notice: %s<br />" %i
            for i in botnet.irc_privmsg :
                print "privmsg: %s<br />" % i
            print "</body>"
            print "</html>"
