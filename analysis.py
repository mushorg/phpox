import hashlib
from datetime import datetime

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

class DataAnalysis(object):

    def __init__(self, script):
        self.botnet = Botnet(script)
        
    def analyze(self, output):
        for line in output.split("\n"):
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