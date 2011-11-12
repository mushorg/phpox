from random import choice
list1 = ["qazwwqw", "qwdewqewqxsdw", "sdadwd", "asdsdwqd", "qwdxswd",
         "asdwq", "qwedqwde", "awdqwd", "qwdwd","wewefdef"]
list2 = ["sdsd", "sdsd", "asdsdwqd", "qwdxswd",
         "asdwq", "qwedqwde", "awdqwd", "qwdwd","wewefdef"]
def call():
    hostname = choice(list1)
    number = choice(list2)
    ret = """
    \treturn 'Linux %s 2.6.38-%s-generic #49-Ubuntu SMP Mon Aug 29 20:47:58 UTC 2011 i686';
    """ % (hostname, number)
    return ret
#print call()