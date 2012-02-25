"""apd_generate.py
apd_generate.py generates apd_sandbox.php
"""
#!/usr/bin/env python
import random
import apd_functions
from replacement import shell_sandbox
from php import utils as php_utils


def output(s):
    print s

php_utils = php_utils.util_functions()
FUNCTIONS = apd_functions.FUNCTIONS

output("<?php\nif(!extension_loaded('apd')) {\n\tdl('apd.so');\n}\n")
output(php_utils.gen_utils_functions())
output(shell_sandbox.shell_sandbox())
int_name = 0
for function, return_val in FUNCTIONS.items():
    parts = function.split(";")
    function_name = parts[0]
    function_args = ", ".join(parts[1:-1])
    rand_int = random.randint(100, 999)
    output("rename_function('%s', '%s_%s');" % (function_name,
                                                function_name, rand_int))
    output("override_function('%s', '%s', 'return %s_rep(%s);');" %
           (function_name, function_args, function_name, function_args))
    output("function %s_rep(%s) {" % (function_name, function_args))
    output("\t$rand = '%s';" % rand_int)
    if return_val == "None":
        return_val = "\treturn;"
    output(return_val)
    output("}")
    output("rename_function('__overridden__', '%s');\n" % int_name)
    int_name += 1

find_irc_server = php_utils.get_symbol('find_irc_server')
output("%s($argv[1]);\n" % find_irc_server)
php_utils.clean()

output("\ninclude $argv[1];\n?>")
