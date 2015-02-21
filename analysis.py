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
import string
from lxml import etree


class Botnet(object):
    """  this class contains irc bot info"""
    def __init__(self, script):
        self.id = ""
        if '/' in script:
            self.file_name = script.rsplit("/", 1)[1]
        else:
            self.file_name = script
        self.file_md5 = hashlib.md5(open(script).read()).hexdigest()
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
        'id': self.id,
        'file_name': self.file_name,
        'file_md5': self.file_md5,
        'first_analysis_date': self.first_analysis_date,
        'last_analysis_date': self.last_analysis_date,
        'irc_addr': self.irc_addr,
        'irc_server_pwd': self.irc_server_pwd,
        'irc_nick': self.irc_nick,
        'irc_user': self.irc_user,
        'irc_mode': self.irc_mode,
        'irc_channel': self.irc_channel,
        'irc_nickserv': self.irc_nickserv,
        'irc_notice': self.irc_notice,
'irc_privmsg': self.irc_privmsg
        }
        return botnet_dict

    @classmethod
    def replace_control(cls, s):
        new_s = ''
        for c in s:
            #replace all control charactors.
            #XXX: this algorithm waste much computational time.
            if c in string.printable:
                new_s += c
            else:
                new_s += '\\%X' % ord(c)
        return new_s

    def toxml(self):
        xml = etree.Element('xml')
        first_analysis_date = etree.Element('first_analysis_date')
        xml.append(first_analysis_date)
        first_analysis_date.text = self.first_analysis_date
        last_analysis_date = etree.Element('last_analysis_date')
        xml.append(last_analysis_date)
        last_analysis_date.text = self.last_analysis_date
        file_md5 = etree.Element('file_md5')
        xml.append(file_md5)
        file_md5.text = self.file_md5
        bot = etree.Element('bot')
        xml.append(bot)
        host = etree.Element('host')
        bot.append(host)
        if len(self.irc_addr) > 0:
            host.text = self.irc_addr
        irc_server_pwd = etree.Element('irc_server_pwd')
        bot.append(irc_server_pwd)
        if len(self.irc_server_pwd) > 0:
            irc_server_pwd.text = etree.CDATA(self.irc_server_pwd)
        irc_nick = etree.Element('irc_nick')
        bot.append(irc_nick)
        if len(self.irc_nick) > 0:
            irc_nick.text = etree.CDATA(self.irc_nick)
        irc_user = etree.Element('irc_user')
        bot.append(irc_user)
        if len(self.irc_user) > 0:
            irc_user.text = self.irc_user
        irc_mode = etree.Element('irc_mode')
        bot.append(irc_mode)
        if len(self.irc_mode) > 0:
            irc_mode.text = self.irc_mode
        irc_nickserv = etree.Element('irc_nickserv')
        bot.append(irc_nickserv)
        if len(self.irc_nickserv) > 0:
            irc_nickserv.text = etree.CDATA(irc_nickserv)
        irc_channels = etree.Element('irc_channels')
        bot.append(irc_channels)
        if len(self.irc_channel) > 0:
            for i in self.irc_channel:
                irc_channel = etree.Element('irc_channel')
                irc_channels.append(irc_channel)
                irc_channel.text = self.replace_control(i)
        else:
            irc_channels.append(etree.Element('irc_channel'))
        irc_notices = etree.Element('irc_notices')
        bot.append(irc_notices)
        if len(self.irc_notice) > 0:
            for i in self.irc_notice:
                irc_notice = etree.Element('irc_notice')
                irc_notices.append(irc_notice)
                irc_notice.text = i
        else:
            irc_notices.append(etree.Element('irc_notice'))
        irc_privmsgs = etree.Element('irc_privmsgs')
        bot.append(irc_privmsgs)
        if len(self.irc_privmsg) > 0:
            for i in self.irc_privmsg:
                irc_privmsg = etree.Element('irc_privmsg')
                irc_privmsgs.append(irc_privmsg)
                irc_privmsg.text = etree.CDATA(self.replace_control(i))
        else:
            irc_privmsgs.append(etree.Element('irc_privmsg'))
        return etree.tostring(xml, encoding="UTF-8",
                              method='xml', xml_declaration=True)


class DataAnalysis(object):
    """this class is used to extracts raw sandbox data to useful info for us"""
    def __init__(self, script, debug=0):
        self.botnet = Botnet(script)
        self.debug_level = debug

    def analyze(self, output):
        for line in output.split("\n"):
            if self.debug_level > 0:
                print repr(line)
            try:
                line = line.decode("windows-1252").strip()
            except UnicodeDecodeError:
                continue
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
