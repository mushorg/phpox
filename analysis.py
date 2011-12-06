import hashlib
import cgi
from datetime import datetime
from xml.dom.minidom import Document

class Botnet(object):
    
    def __init__(self, script):
        self.file_name = script.rsplit("/", 1)[1]
        self.file_md5 = hashlib.md5(open(script).read()).hexdigest()
        self.analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.irc_addr = ""
        self.irc_server_pwd = ""
        self.irc_nick = ""
        self.irc_user = ""
        self.irc_mode = ""
        self.irc_channel = []
        self.irc_nickserv = ""
        self.irc_notice = []
        self.irc_privmsg = []

    def toxml(self):
        doc = Document()
        xml = doc.createElement('xml')
        doc.appendChild(xml)
        analysis_date = doc.createElement('analysis_date')
        xml.appendChild(analysis_date)
        analysis_date.appendChild(doc.createTextNode(self.analysis_date))
        file_md5 = doc.createElement('file_md5')
        xml.appendChild(file_md5)
        file_md5.appendChild(doc.createTextNode(self.file_md5));
        bot = doc.createElement('bot')
        xml.appendChild(bot)
        host = doc.createElement('host')
        bot.appendChild(host)
        if( len(self.irc_addr) > 0):
            host.appendChild(doc.createTextNode(self.irc_addr))
        irc_server_pwd = doc.createElement('irc_server_pwd')
        bot.appendChild(irc_server_pwd)
        if( len(self.irc_server_pwd) > 0):
            irc_server_pwd.appendChild(doc.createTextNode(self.irc_server_pwd))
        irc_nick = doc.createElement('irc_nick')
        bot.appendChild(irc_nick)
        if( len(self.irc_nick) > 0):
            irc_nick.appendChild(doc.createTextNode(self.irc_nick))
        irc_user = doc.createElement('irc_user')
        bot.appendChild(irc_user)
        if( len(self.irc_user) > 0):
            irc_user.appendChild(doc.createTextNode(self.irc_user))
        irc_mode = doc.createElement('irc_mode')
        bot.appendChild(irc_mode)
        if(len(self.irc_mode)>0):
            irc_mode.appendChild(doc.createTextNode(self.irc_mode))
        irc_nickserv = doc.createElement('irc_nickserv')
        bot.appendChild(irc_nickserv)
        if(len(self.irc_nickserv)> 0):
            irc_nickserv.appendChild(doc.createTextNode(self.irc_nickserv))
        irc_channels = doc.createElement('irc_channels')
        bot.appendChild(irc_channels)
        if( len(self.irc_channel) > 0):
            for i in self.irc_channel:
                irc_channel = doc.createElement('irc_channel')
                irc_channels.appendChild(irc_channel)
                irc_channel.appendChild(doc.createTextNode(i))
        else:
            irc_channels.appendChild(doc.createElement('irc_channel'))
        irc_notices = doc.createElement('irc_notices')
        bot.appendChild(irc_notices)
        if( len(self.irc_notice) > 0):
            for i in self.irc_notice:
                irc_notice = doc.createElement('irc_notice')
                irc_notices.appendChild(irc_notice)
                irc_notice.appendChild(doc.createTextNode(i))
        else:
            irc_notices.appendChild(doc.createElement('irc_notice'))
        irc_privmsgs = doc.createElement('irc_privmsgs')
        bot.appendChild(irc_privmsgs)
        if( len(self.irc_privmsg) > 0):
            for i in self.irc_privmsg:
                irc_privmsg = doc.createElement('irc_privmsg')
                irc_privmsgs.appendChild(irc_privmsg)
                irc_privmsg.appendChild(doc.createTextNode(i))
        else:
            irc_privmsgs.appendChild(doc.createElement('irc_privmsg'))
        return doc.toprettyxml(indent = " ")

class DataAnalysis(object):

    def __init__(self, script, debug=0):
        self.botnet = Botnet(script)
        self.debug_level = debug
        
    def analyze(self, output):
        for line in output.split("\n"):
            if( self.debug_level> 0):
                print repr(line)
            line = line.decode("windows-1252")
            if line[:4] == "ADDR":
                self.botnet.irc_addr = line[5:]
            elif line[:4] == "PASS":
                self.botnet.irc_server_pwd = line[5:]
            elif line[:4] == "USER":
                self.botnet.irc_user = line[5:]
            elif line[:4] == "NICK":
                self.botnet.irc_nick = line[5:]
            elif line[:4] == "MODE":
                try:
                    self.botnet.irc_mode = line[5:].split(" ", 1)[1]
                except(IndexError):
                    continue
            elif line[:4] == "JOIN":
                self.botnet.irc_channel.append(line[5:])
            elif line[:7] == "PRIVMSG":
                line_parts = line[8:].split(" ")
                if line_parts[0] == "nickserv":
                    self.botnet.irc_nickserv = line[8:]
                else:
                    self.botnet.irc_privmsg.append(line[8:])
            elif line[:6] == "NOTICE":
                self.botnet.irc_notice.append(line[7:])
            
        return self.botnet
