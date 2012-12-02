import sys
import hashlib
import os
import base64

from datetime import datetime

import hpfeed.hpfeeds as hpfeeds
import apd_sandbox as sandbox


class HPFeedsSink(object):

    def __init__(self):
        self.host = 'hpfeeds.honeycloud.net'
        self.port = 10000
        self.channels = ['glastopf.files', ]
        self.ident = ''
        self.secret = ''
        self.sb = sandbox.PHPSandbox()

    def log(self, msg):
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print '[hpf sink {0}] {1}'.format(time_stamp, msg)

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
        return file_name

    def run(self):
        hps = HPFeedsSink()
        try:
            self.hpc = hpfeeds.new(hps.host, hps.port, hps.ident, hps.secret)
        except hpfeeds.FeedException, e:
            self.log('Feed exception: %s' % e)
            return 1

        self.log('Connected to: %s' % self.hpc.brokername)

        def on_message(identifier, channel, payload):
            if channel == "glastopf.files":
                try:
                    file_name = hps.store_file(
                        base64.b64decode(str(payload).split(' ', 1)[1]))
                except TypeError as e:
                    self.log('TypeError: %s' % str(e))
                else:
                    self.log("Analyzing file %s" % file_name)
                    self.sb.sandbox('files/' + file_name, 10)

        def on_error(payload):
            self.log('Error message from server: {0}'.format(payload))
            self.hpc.stop()

        self.hpc.subscribe(hps.channels)
        try:
            self.hpc.run(on_message, on_error)
        except hpfeeds.FeedException, e:
            self.log('Feed exception: %s' % e)
        except KeyboardInterrupt:
            pass
        finally:
            self.hpc.close()
        return 0

if __name__ == '__main__':
    hs = HPFeedsSink()
    try:
        sys.exit(hs.run())
    except KeyboardInterrupt:
        sys.exit(0)
