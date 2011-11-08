import SocketServer
import time
import brute

class FakeServer(SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, filename):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.filename = filename
        self.timeout = 2

class RequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        sample_string = brute.open_sample(self.server.filename)
        pw_list = brute.find_strings(sample_string)
        self.request.send(":ircserver NOTICE * :*** SomeString \n")
        self.request.send(":ircserver 001 nick :SomeString \n")
        self.request.send(":ircserver 004 nick SomeString \n")
        while True:
            data = self.request.recv(1024)
            print data
            if "JOIN" in data:
                channel = "#" + data.partition("#")[2].split(" ")[0].strip()
                print "channel", repr(channel)
                for pw in pw_list:
                    msg = ":owner!name@address PRIVMSG " + channel + " :.user " + pw
                    print "message", repr(msg)
                    try:
                        self.request.send(msg)
                    except Exception as e:
                        print "exception message:" + e.message                                            
                    time.sleep(0.1)
                    data = self.request.recv(10)
                    print data
                    if pw == "planetworkteams":
                        break
    
            else:
                time.sleep(3)
        return

class FakeListener(object):
    
    def main(self, filename):
        address = ('localhost', 1234)
        server = FakeServer(address, RequestHandler, filename)
        return server