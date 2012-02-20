import sys
from ConfigParser import ConfigParser

if __name__ == '__main__':
    import hpfeeds
else:
    import hpfeed.hpfeeds as hpfeeds


class HPFeedClient(object):

    def __init__(self, pre):
        conf_parser = ConfigParser()
        conf_parser.read(pre + "apd_sandbox.cfg")
        self.host = conf_parser.get("hpfeed", "host")
        self.port = int(conf_parser.getint("hpfeed", "port"))
        self.channels = conf_parser.get("hpfeed", "chan").encode('latin1').split(',')
        self.ident = conf_parser.get("hpfeed", "ident").encode('latin1').strip()
        self.secret = conf_parser.get("hpfeed", "secret").encode('latin1')

    def log(self, msg):
        print '[hpf feed] {0}'.format(msg)

    def run(self):
        try:
            self.hpc = hpfeeds.new(self.host, self.port, self.ident, self.secret)
        except hpfeeds.FeedException, e:
            self.log('Feed exception: %s' % e)
            return 1

        self.log('Connected to: %s' % self.hpc.brokername)

        def on_message(identifier, channel, payload):
            pass

        def on_error(payload):
            self.log('Error message from server: {0}'.format(payload))
            self.hpc.stop()

        try:
            self.hpc.run(on_message, on_error)
        except hpfeeds.FeedException, e:
            self.log('Feed exception: %s' % e)
        except KeyboardInterrupt:
            pass
        finally:
            self.hpc.close()
        return 0

    def publish(self, channel, data):
        self.hpc.publish(channel, data)
        self.log('Analysis data published to feed')
        self.hpc.stop()
        self.hpc.close()

if __name__ == '__main__':
    hs = HPFeedClient('../')
    try:
        sys.exit(hs.run())
    except KeyboardInterrupt:
        sys.exit(0)
