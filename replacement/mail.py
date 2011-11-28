from email.parser import Parser

headers = Parser().parsestr('From: <user@example.com>\n'
        'To: <someone_else@example.com>\n'
        'Subject: Test message\n'
        'Message: Send Successfully\n')

#print 'To: %s' % headers['to']
#print 'From: %s' % headers['from']
#print 'Subject: %s' % headers['subject']
#print 'message: %s' % headers['message']
def call():
    ret = """
    \t string {0} , string {1} , string {2}, string {3}
    """.format(headers['to'], headers['From'],headers['Subject'], headers['Message'])
    print ret
    return bool(ret)
print call()