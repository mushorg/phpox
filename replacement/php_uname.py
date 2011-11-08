from random import choice

def call():
    hostname = choice(["Server", "Momo"])
    number = choice(["11", "12"])
    ret = """
    \treturn 'Linux %s 2.6.38-%s-generic #49-Ubuntu SMP Mon Aug 29 20:47:58 UTC 2011 i686';
    """ % (hostname, number)
    return ret