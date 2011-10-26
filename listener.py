import SocketServer
import socket
import threading
import time
import brute

class EchoRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        
        sample_string = brute.open_sample("samples/get/204df484ad6d09f5bb03b8152216e6c0")
        pw_list = brute.find_strings(sample_string)
        # Echo the back to the client
        self.request.send(":ircserver NOTICE * :*** SomeString \n")
        self.request.send(":ircserver 001 nick :SomeString \n")
        self.request.send(":ircserver 004 nick SomeString \n")
        while True:
            data = self.request.recv(1024)
            print data
            if "JOIN" in data:
                channel = "#" + data.partition("#")[2].split(" ")[0].strip()
                print channel
                for pw in pw_list:
                    print repr(pw)
                    msg = ":owner!name@address PRIVMSG " + channel + " :.user " + pw
                    print repr(msg)
                    self.request.send(msg)
                    time.sleep(1)
                    if pw == "aank1234":
                        break
    
            else:
                time.sleep(1)
        return

if __name__ == '__main__':
    address = ('localhost', 1234) # let the kernel give us a port
    server = SocketServer.TCPServer(address, EchoRequestHandler)
    ip, port = server.server_address # find out what port we were given

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(False)
    t.start()