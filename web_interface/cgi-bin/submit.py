#!/usr/bin/env python

# Copyright (C) 2012  Lukas Rist
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

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
    <input type="file"  name="filename" />
    <input type="radio" name="xml" value="0" checked><b>HTML</b></font></input>
    <input type="radio" name="xml" value="1"><b>XML</intput>
    <input type="submit" name="submit" />
    </form>
    """

form = cgi.FieldStorage()

if not form:
    print "Content-type: text/html"
    print
    print """
    <html>
    <head><title>Test upload pages</title></head>
    <body >          
     <div id = "logo" style="text-align:left;position:relative;top:-10px;">
         <img height="250px" width="350px" src="../images/Logo.png"/>   
     </div> 
     <div id = "upload" style="text-align:center; position:relative;top:-200px;" > 
     <p /><br />""" + form_body() + """
    </div>
    
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
            print "<html><head><title>Test Upload page</title></head>"
            print "<body>"
            print "<div id = 'logo' style='text-align:left;position:relative;top:-10px;'>"
            print "<img height='250px' width='350px' src='../images/Logo.png'/>"
            print "</div>" 
            print "<div id = 'upload' style='text-align:center; position:relative;top:-200px;' >"
            print "<p /><br />"
            print form_body()
            print "</div>"
            print "<div id = 'data' style='text-align:left; position:relative;top:-100px;' > "
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
