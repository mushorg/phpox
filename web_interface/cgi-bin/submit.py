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
    <div id = "background" align="center">
    <input type="file"  name="filename" />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <input type="radio" name="xml" value="0"> <font color="#EEEE00"><b>HTML</b></font></input>
    <input type="radio" name="xml" value="1"><font color="#EEEE00"><b>XML</intput>
    <p/><input type="submit" name="submit" />
    </div>
    </form>
    """

form = cgi.FieldStorage()

if not form:
    print "Content-type: text/html"
    print
    print """
    <html>
    <head><title>Test upload pages</title></head>
    <link href="style.css" rel="stylesheet" type="text/css" media="screen" />
    <body  align="center" style="background-color:#FFFFFF"; >
    <div id = "background" height="200px" width="700px"  align="center" >
        <div id="sandboxlogo" >
             <img height="125px" width="250px" src="images/PHP_SandBox_log.png"/>   
             <img height="125px" width="600px" src="images/load.png"/><p/>
        </div> 
    </div> 
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
            print botnet.toxml()
        else:
            print "Content-type: text/html"
            print 
            print "<html>"
            print "<body>"
            print form_body()
            print "first analysis date: %s<br />" % botnet.first_analysis_date
            print "last analysis date: %s<br />" % botnet.last_analysis_date
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
