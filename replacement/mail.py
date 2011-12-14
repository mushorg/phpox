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
    echo "MAIL $to $subject $message\\n";
    return TRUE;
    """
    return ret
