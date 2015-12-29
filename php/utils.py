# Copyright (C) 2012 Lukas Rist
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
import string
import json
import os
from string import Template


class UtilFunctions(object):
    def __init__(self, prefix='php/'):
        self.prefix = prefix
        self.symbol_table = {}
        # initialed in read_json()
        self.used_name = []
        self.jfile = None
        self.gen_utils_functions()

    @classmethod
    def clean(cls):
        os.unlink('/tmp/php_utils_table_%d' % os.getpid())
        os.unlink('/tmp/php_utils_scripts_%d' % os.getpid())

    def gen_utils_functions(self):
        # xXx it's ULTRA UGLY!!!
        # Because the replacement/xxx.call() is called in very early stage.
        # Those function codes execute when importing apd_function.py
        # Thus I have problem to pass the real symbols into those functions.
        try:
            fd = open('/tmp/php_utils_table_%d' % os.getpid(), 'r')
            j_code = fd.read()
            fd.close()

            obj = json.loads(j_code)
            self.symbol_table = obj['symbol_table']
            self.used_name = obj['used_name']
            fd = open('/tmp/php_utils_scripts_%d' % os.getpid(), 'r')
            ret = fd.read()
            fd.close()
        except:
            ret = ''
            # the order is very important!!!
            ret += self.def_string_parser()
            ret += self.def_multiple_irc()
            obj = {
                'used_name': self.used_name,
                'symbol_table': self.symbol_table,
            }
            fd = open('/tmp/php_utils_table_%d' % os.getpid(), 'w')
            fd.write(json.dumps(obj))
            fd.close()
            fd = open('/tmp/php_utils_scripts_%d' % os.getpid(), 'w')
            fd.write(ret)
            fd.close()
        return ret

    def get_symbol(self, name=None):
        if name is None:
            return self.symbol_table
        else:
            return self.symbol_table[name]

    def symbol_append(self, symbol, masq):
        if symbol in self.symbol_table:
            raise BaseException('Name collaps: %s' % symbol)
        self.symbol_table[symbol] = masq
        self.used_name.append(masq)

    def generate_random_name(self):
        ret = ''
        while True:
            prefix = '' . join(random.choice((string.ascii_uppercase + string.ascii_lowercase)) for x in range(3))
            postfix = '' . join(random.choice(
                (string.ascii_uppercase + string.ascii_lowercase + string.digits))
                for x in range(5))
            if prefix + postfix not in self.used_name:
                ret = (prefix + postfix)
                break
        return ret

    def def_string_parser(self):
        ret = ''
        replacement = dict(simple_code_parser='')
        replacement['simple_code_parser'] = self.generate_random_name()
        self.symbol_append('simple_code_parser', replacement['simple_code_parser'])
        # self.symbol_table['simple_code_parser'] = replacement['simple_code_parser']
        with open(self.prefix + "string_paser.template") as fd:
            line = ''
            for l in fd.readlines():
                line += l
        t = Template(line)
        ret += t.substitute(replacement)
        return ret

    def def_multiple_irc(self):
        ret = ''
        replacement = {
            'multiple_irc': '',
            'parsed_strings': '',
            'find_irc_server': '',
            'multiple_irc_return_false': '',
            # it should be generated.
            'simple_code_parser': '',
        }
        replacement['multiple_irc'] = self.generate_random_name()
        self.symbol_append('multiple_irc', replacement['multiple_irc'])
        replacement['parsed_strings'] = self.generate_random_name()
        self.symbol_append('parsed_strings', replacement['parsed_strings'])
        replacement['find_irc_server'] = self.generate_random_name()
        self.symbol_append('find_irc_server', replacement['find_irc_server'])
        replacement['multiple_irc_return_false'] = self.generate_random_name()
        self.symbol_append('multiple_irc_return_false', replacement['multiple_irc_return_false'])
        replacement['simple_code_parser'] = self.get_symbol('simple_code_parser')
        with open(self.prefix + "multiple_irc.template") as fd:
            line = ''
            for l in fd.readlines():
                line += l
        t = Template(line)
        ret += t.substitute(replacement)
        return ret

# testing program
if __name__ == "__main__":
    utils = UtilFunctions(prefix='')
    print(utils.gen_utils_functions())
    print("%s();" % utils.get_symbol(name='simple_code_parser'))
    utils.clean()
