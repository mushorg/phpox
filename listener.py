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
import threading

import brute


class FakeServer(SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, stopit):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.stopit = stopit


class RequestHandler(SocketServer.BaseRequestHandler):

    def brute_pw(self, data):
        pw_list = ["foo", "bar", "planetworkteams"]
        channel = "#" + data.partition("#")[2].split(" ")[0].strip()
        for pw in pw_list:
            msg = ":owner!name@address PRIVMSG " + channel + " :.user " + pw + "\n"
            try:
                self.request.send(msg)
                msg = ":owner!name@address PRIVMSG " + channel + " :.info\n"
                self.request.send(msg)
            except Exception as e:
                print "exception message:", e
            time.sleep(0.1)

    def handle(self):
        #pw_list = brute.find_strings()
        self.request.send(":ircserver NOTICE * :*** SomeString \n")
        self.request.send(":ircserver 001 nick :SomeString \n")
        self.request.send(":ircserver 004 nick SomeString \n")
        while not self.server.stopit.is_set():
            data = self.request.recv(1024)
            if len(data) > 0:
                self.request.send(data.strip() + "\n")
            if "JOIN" in data:
                pass
                #self.brute_pw(data)
            else:
                time.sleep(1)
        return


class ListenerThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name,
                                  verbose=verbose)
        self.setDaemon(True)
        self.args = args
        self.kwargs = kwargs
        self.stopit = threading.Event()

    def run(self):
        address = ('localhost', 1234)
        server = FakeServer(address, RequestHandler, self.stopit)
        server.serve_forever()

    def stop(self):
        self.stopit.set()
