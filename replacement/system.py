from string import Template
import random

def call():
    # TODO: Make uptime dynamic
    function = Template("""
    $$parts = explode(';', $$cmd);
    foreach ($$parts as $$part){
        $$cmd_part = explode(' ', $$part);
        print_r($$cmd_part);
    }
    if ($$cmd == 'id') {
        $$ret = array('uid=0(root) gid=0(root) groups=0(root)',);
    }elseif ($$cmd == 'uptime') {
        $$ret = array('16:12:55 up 152 days, 19:03,  0 user,  load average: 0.02, 0.02, 0.03',);
    }\n\telseif ($$cmd == 'cat /proc/cpuinfo') { \n
    $$ret = array('processor	: 0
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
CPU1:		online
', 0);
    }else {
        $$ret = array('None',);
    }
    return $$ret;""")
    parameter_dict = {
                      "manufacturer" : ["TI", "Lukas Corp", "Spots Garage"],
                      }
    ret_string = function.substitute(manufacturer = random.choice(parameter_dict['manufacturer']))
    return ret_string