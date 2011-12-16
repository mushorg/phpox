#from email.parser import Parser

#headers = Parser().parsestr('From: <user@example.com>\n'
        #'To: <someone_else@example.com>\n'
        #'Subject: Test message\n'
        #'Message: Send Successfully\n')

def call(): 
    function = """
    \t$function_name = "mail_" . $rand;
    \t\treturn $function_name;
    """ 
    return function 
#print call()
