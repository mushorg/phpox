#!/usr/bin/env python3

# Copyright (C) 2015 Lukas Rist
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import random
import functions
from replacement import shell_sandbox
from php import utils as php_utils


php_utils = php_utils.UtilFunctions()
FUNCTIONS = functions.FUNCTIONS

print("<?php\nif(!extension_loaded('bfr')) {\n\tdl('bfr.so');\n}\n")
print("error_reporting(E_ALL ^ E_WARNING ^ E_NOTICE);\n\n")
print(php_utils.gen_utils_functions())
print(shell_sandbox.shell_sandbox())
for function, return_val in FUNCTIONS.items():
    parts = function.split(";")
    function_name = parts[0]
    function_args = ", ".join(parts[1:-1])
    rand_int = random.randint(100, 999)
    print("rename_function('%s', '%s_%s');" % (function_name, function_name, rand_int))
    print(
        "override_function('%s', '%s', 'return %s_rep(%s);');"
        % (function_name, function_args, function_name, function_args)
    )
    print("function %s_rep(%s) {" % (function_name, function_args))
    print("\t$rand = '%s';" % rand_int)
    if return_val == "None":
        return_val = "\treturn;"
    print(return_val)
    print("}")

find_irc_server = php_utils.get_symbol("find_irc_server")
print("%s($argv[1]);\n" % find_irc_server)
php_utils.clean()

print("\ninclude $argv[1];\n?>")
