from random import choice
from datetime import datetime
# TODO replace random string with actual content
hosts = ["Linux", "Server", "WebServer","FTP","SMTP","POP3","Unix" ]
version_numbers = ["3.0.0.12.14","2.6.24.29.31","2.6.32.35.41","2.6.35.30.39","2.6.38.12.27","3.1.0.2.2"]
date = datetime.now().strftime("%a %b %d %H:%M:%S UTC %Y")
str1 = ["#41","#42","#43","#44","#45","#46","#47","#48","#49"]
version_name=["Fedora","Redhat","CenOs","FreeBSD","Mandriva","Debian","Gentoo","SUSE"]
kernel_version=["i386","i686"]
def call():
    hostname = choice(hosts)
    number = choice(version_numbers)
    str2=choice(str1)
    name = choice(version_name)
    kernel=choice(kernel_version)
    ret = """
    \treturn 'Linux {0} {1}-generic {2}-{3} SMP {4} {5}';
    """.format(hostname, number,str2,name,date,kernel)
    return ret
print call()