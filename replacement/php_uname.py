from random import choice
from datetime import datetime

# TODO replace random string with actual content
hosts = ["Linux", "Server", "WebServer", ]
version_numbers = ["2.6.38-2",]

date = datetime.now().strftime("%a %b %d %H:%M:%S UTC %Y")

def call():
    hostname = choice(hosts)
    number = choice(version_numbers)
    ret = """
    \treturn 'Linux {0} {1}-generic #49-Ubuntu SMP {2} i686';
    """.format(hostname, number, date)
    return ret
#print call()