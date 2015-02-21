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

import time
from gevent.server import StreamServer
import gevent


class FakeListener():

    def __init__(self):
        self.server = StreamServer(('127.0.0.1', 1234), self.handle)

    def brute_pw(self, data, socket):
        pw_list = ["foo", "bar", "planetworkteams"]
        channel = "#" + data.partition("#")[2].split(" ")[0].strip()
        for pw in pw_list:
            msg = ":owner!name@address PRIVMSG " + channel + " :.user " + pw + "\n"
            try:
                socket.send(msg)
                msg = ":owner!name@address PRIVMSG " + channel + " :.info\n"
                socket.send(msg)
            except Exception as e:
                print "exception message:", e
            time.sleep(0.1)

    def handle(self, socket, address):
        #pw_list = brute.find_strings()
        socket.send(":ircserver NOTICE * :*** SomeString \n")
        socket.send(":ircserver 001 nick :SomeString \n")
        socket.send(":ircserver 004 nick SomeString \n")
        while True:
            data = socket.recv(1024)
            if len(data) > 0:
                socket.send(data.strip() + "\n")
            if "JOIN" in data:
                pass
            else:
                time.sleep(1)
        return

    def run(self):
        return gevent.spawn(self.server.start)

