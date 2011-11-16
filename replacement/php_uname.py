from random import choice
from datetime import datetime
# TODO replace random string with actual content
hosts = ["Linux", "Server", "WebServer", "FTP", "SMTP", "POP3", "Unix" ]
version_numbers = ["3.0.0-14", "2.6.24-29", "2.6.32-41", "2.6.35-30", "2.6.38-7", "3.1.0-2"]
date = datetime.now().strftime("%a %b %d %H:%M:%S UTC %Y")
str1 = ["#41", "#42", "#43", "#44", "#45", "#46", "#47", "#48", "#49"]
#version_name = ["Fedora", "Redhat", "CentOs", "FreeBSD", "Mandriva", "Debian", "Gentoo", "SUSE"]

kernel_version = ["i386", "i686"]
operating_system = ["GNU/Linux", "GNU/Unix"]
def call():
    hostname = choice(hosts)
    number = choice(version_numbers)
    str2 = choice(str1)
    s1 = "-generic %s-Ubuntu" % str2
    s2 = " %s CentOs" % str2
    version= [s1,s2]
    version_choice = choice (version) 
    #name = choice(version_name)
    kernel = choice(kernel_version)
    operating = choice(operating_system)
    ret = """
    \treturn 'Linux {0} {1}{2} SMP {3} {4} {5}';
    """.format(hostname, number, version_choice,  date, kernel, operating)
    return ret
print call()