"""listener.py
listener.php is intend to be a fake irc server , pretend to be the irc server 
which bots trying to connect. listener.py is similar to listener.php but trying
 to catch the botnet password with brute.py function. 
"""

import SocketServer
import time
import brute

class FakeServer(SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, filename):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.filename = filename

class RequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        pw_list = brute.find_strings(self.server.filename)
        self.request.send(":ircserver NOTICE * :*** SomeString \n")
        self.request.send(":ircserver 001 nick :SomeString \n")
        self.request.send(":ircserver 004 nick SomeString \n")
        while True:
            data = self.request.recv(1024)
            print data, "\n"
            if "JOIN" in data:
                channel = "#" + data.partition("#")[2].split(" ")[0].strip()
                for pw in pw_list:
                    msg = ":owner!name@address PRIVMSG " + channel + " :.user " + pw
                    try:
                        self.request.send(msg)
                    except Exception as e:
                        print "exception message:", e                                            
                    time.sleep(0.1)
    
            else:
                time.sleep(3)
        return

class FakeListener(object):
    
    def main(self, filename):
        address = ('localhost', 1234)
        server = FakeServer(address, RequestHandler, filename)
        return server
