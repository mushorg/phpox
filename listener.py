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

import SocketServer
import time
import brute


class FakeServer(SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, filename):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.filename = filename


class RequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        #pw_list = brute.find_strings(self.server.filename)
        pw_list = ["foo", "bar"]
        self.request.send(":ircserver NOTICE * :*** SomeString \n")
        self.request.send(":ircserver 001 nick :SomeString \n")
        self.request.send(":ircserver 004 nick SomeString \n")
        while True:
            data = self.request.recv(1024)
            self.request.send(data)
            if "JOIN" in data:
                channel = "#" + data.partition("#")[2].split(" ")[0].strip()
                for pw in pw_list:
                    msg = ":owner!name@address PRIVMSG " + channel + " :.user " + pw + "\n"
                    try:
                        self.request.send(msg)
                    except Exception as e:
                        print "exception message:", e
                    time.sleep(0.1)
            else:
                time.sleep(1)
        return


class FakeListener(object):

    def main(self, filename=None):
        address = ('localhost', 1234)
        server = FakeServer(address, RequestHandler, filename)
        return server


if __name__ == "__main__":
    listener = FakeListener()
    server = listener.main()
    server.serve_forever()
