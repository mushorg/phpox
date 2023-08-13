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

import hashlib


class Botnet(object):
    """this class contains irc bot info"""

    def __init__(self, script):
        self.id = ""
        if "/" in script:
            self.file_name = script.rsplit("/", 1)[1]
        else:
            self.file_name = script
        self.file_md5 = hashlib.md5(open(script).read().encode("utf-8")).hexdigest()
        self.first_analysis_date = ""
        self.last_analysis_date = ""
        self.irc_addr = ""
        self.irc_server_pwd = ""
        self.irc_nick = ""
        self.irc_user = ""
        self.irc_mode = ""
        self.irc_channel = []
        self.irc_nickserv = ""
        self.irc_notice = []
        self.irc_privmsg = []

    def todict(self):
        botnet_dict = {
            "id": self.id,
            "file_name": self.file_name,
            "file_md5": self.file_md5,
            "first_analysis_date": self.first_analysis_date,
            "last_analysis_date": self.last_analysis_date,
            "irc_addr": self.irc_addr,
            "irc_server_pwd": self.irc_server_pwd,
            "irc_nick": self.irc_nick,
            "irc_user": self.irc_user,
            "irc_mode": self.irc_mode,
            "irc_channel": self.irc_channel,
            "irc_nickserv": self.irc_nickserv,
            "irc_notice": self.irc_notice,
            "irc_privmsg": self.irc_privmsg,
        }
        return botnet_dict


class DataAnalysis(object):
    """this class is used to extracts raw sandbox data to useful info for us"""

    def __init__(self, script, debug=0):
        self.botnet = Botnet(script)
        self.debug_level = debug

    def analyze(self, output):
        output = output.decode("utf-8")
        for line in output.split("\n"):
            if self.debug_level > 0:
                print(repr(line))
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
                except IndexError:
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
