from string import Template
import random
def shell_sandbox():
   function = Template("""
function shell_sandbox($$cmd){
 $$ret = array('None',);
 $$parts = explode(';', $$cmd);
 foreach ($$parts as $$part){
     $$cmd_part = explode(' ', $$part);
 #    print_r($$cmd_part);
 }
 if ($$cmd == 'id') {
     $$ret = array('uid=0(root) gid=0(root) groups=0(root)',);
 }elseif ($$cmd == 'uptime') {
     $$ret = array('16:12:55 up 152 days, 19:03,  0 user,  load average: 0.02, 0.02, 0.03',);
 }elseif ($$cmd_part[0] == 'cat'){\n
 \t if($$cmd_part[1] == '/proc/cpuinfo') { \n
 \t\t$$ret = array('processor	: 0
cpu		: ${manufacturer} UltraSparc III+ (Cheetah+)
fpu		: UltraSparc III+ integrated FPU
pmu		: ultra3+
prom		: OBP 4.5.21 2003/02/24 17:23
type		: sun4u
ncpus probed	: 2
ncpus active	: 2
D$$ parity tl1	: 0
I$$ parity tl1	: 0
Cpu0ClkTck	: 000000003c7fabc0
Cpu1ClkTck	: 000000003c7fabc0
MMU Type	: Cheetah+
State:
CPU0:		online
CPU1:		online\n', );
  \t}elseif($$cmd_part[1] == '/etc/passwd' ){\n
  \t\t$$ret = array('root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
bin:x:2:2:bin:/bin:/bin/sh
sys:x:3:3:sys:/dev:/bin/sh
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/bin/sh
man:x:6:12:man:/var/cache/man:/bin/sh
lp:x:7:7:lp:/var/spool/lpd:/bin/sh
mail:x:8:8:mail:/var/mail:/bin/sh
news:x:9:9:news:/var/spool/news:/bin/sh
uucp:x:10:10:uucp:/var/spool/uucp:/bin/sh
proxy:x:13:13:proxy:/bin:/bin/sh
www-data:x:33:33:www-data:/var/www:/bin/sh
backup:x:34:34:backup:/var/backups:/bin/sh
list:x:38:38:Mailing List Manager:/var/list:/bin/sh
irc:x:39:39:ircd:/var/run/ircd:/bin/sh
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/bin/sh
nobody:x:65534:65534:nobody:/nonexistent:/bin/sh
libuuid:x:100:101::/var/lib/libuuid:/bin/sh
Debian-exim:x:101:103::/var/spool/exim4:/bin/false
statd:x:102:65534::/var/lib/nfs:/bin/false
sshd:x:103:65534::/var/run/sshd:/usr/sbin/nologin
messagebus:x:104:106::/var/run/dbus:/bin/false
avahi:x:105:107:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/bin/false
${user_in_passwd}:x:10003:1::/home/${user_in_passwd}:/bin/sh\n', );
 \t}
 }
 return $$ret;
}
   """)
   parameter_dict = {
         "manufacturer" : ["TI", "Lukas Corp", "Spots Garage"],
         "user_in_passwd" : ["john", "admin", "peter"],
         }
   ret_string = function.substitute(manufacturer = random.choice(parameter_dict['manufacturer']),
       user_in_passwd = random.choice(parameter_dict['user_in_passwd'])
       )
   return ret_string
