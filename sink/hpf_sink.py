import sys
import hashlib
import os

import sink.hpfeeds as hpfeeds
import apd_sandbox as sandbox


class HPFeedsSink(object):

    def __init__(self):
        self.host = 'hpfeeds.honeycloud.net'
        self.port = 10000
        self.channels = ['glastopf.files', ]
        self.ident = ''
        self.secret = ''

    def get_filename(self, injected_file):
        file_name = hashlib.md5(injected_file).hexdigest()
        return file_name

    def store_file(self, injected_file):
        file_name = self.get_filename(injected_file)
        if not os.path.exists("files/" + file_name):
            with open("files/" + file_name, 'w') as local_file:
                local_file.write(injected_file)
                self.log('File written to diks: {0}'.format(file_name))
        else:
            self.log('File already exists: {0}'.format(file_name))
            file_name = False

    def run(self):
        try:
            hpc = hpfeeds.new(self.host, self.port, self.ident, self.secret)
        except hpfeeds.FeedException, e:
            print >>sys.stderr, 'feed exception:', e
            return 1

        print >>sys.stderr, 'connected to', hpc.brokername

        def on_message(self, identifier, channel, payload):
            if channel == "glastopf.files":
                file_name = self.store_file(str(payload).split(' ', 1)[1])
                print "New file:", file_name
                sandbox.sandbox('files/' + file_name)

        def on_error(self, payload):
            print >>sys.stderr, ' -> errormessage from server: {0}'.format(payload)
            hpc.stop()

        hpc.subscribe(self.channels)
        try:
            hpc.run(on_message, on_error)
        except hpfeeds.FeedException, e:
            print >>sys.stderr, 'feed exception:', e
        except KeyboardInterrupt:
            pass
        finally:
            #cur.close()
            #conn.close()
            hpc.close()
        return 0

if __name__ == '__main__':
    hs = HPFeedsSink()
    try:
        sys.exit(hs.run())
    except KeyboardInterrupt:
        sys.exit(0)
