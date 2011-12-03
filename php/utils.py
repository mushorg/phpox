import random
import string
from string import Template

class util_functions(object):
    def __init__(self):
        self.symbol_table = {} 
        self.used_name = []

    def gen_utils_functions(self):
        ret = ''
        ret += self.def_string_parser()
        return ret

    def get_symbol(self, name=None ):
        if( name is None ):
            return self.symbol_table
        else:
            return self.symbol_table[name]

    def symbol_append(self, symbol, masq):
        if(symbol in self.symbol_table):
            raise BaseException('Name collaps: %s' % symbol)
        self.symbol_table[symbol] = masq


    def generate_random_name(self):
        ret = ''
        while True:
            prefix = '' . join(random.choice((string.ascii_uppercase + string.ascii_lowercase)) for x in range(3))
            postfix = '' . join(random.choice(
                (string.ascii_uppercase + string.ascii_lowercase + string.digits))
                for x in range(5))
            if((prefix + postfix) not in self.used_name):
                ret = (prefix + postfix)
                break
        self.used_name.append(ret)
        return ret

    def def_string_parser(self):
        ret = ''
        replacement = {
            'simple_code_parser':'',
            }
        replacement['simple_code_parser'] = self.generate_random_name()
        self.symbol_append('simple_code_parser', replacement['simple_code_parser'])
        #self.symbol_table['simple_code_parser'] = replacement['simple_code_parser']
        fd = open("php/string_paser.template")
        line = ''
        for l in fd.readlines():
            line += l
        fd.close()
        t = Template(line)

        ret += t.substitute(replacement)
        return ret;
        
#testing program
if __name__ == "__main__":
    utils = util_functions()
    print utils.gen_utils_functions()
    print "%s();" % utils.get_symbol(name='simple_code_parser')
