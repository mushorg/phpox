from php import utils as php_utils
from string import Template
def call():
    utils = php_utils.util_functions()
    multiple_irc_return_false = utils.get_symbol('multiple_irc_return_false')
    T = Template("""\techo "\\nADDR " . $$hostname . ':' . $$port . "\\n";
\t$$multiple_irc_return_false = "${multiple_irc_return_false}";
\tif($$multiple_irc_return_false()){
\t\tif(rand(0,1) == 0){
\t\t\techo "\\nMULTIPLE IRC Server return FALSE\\n";
\t\t\treturn FALSE;
\t\t}
\t}
\t$$function_name = "fsockopen" . "_" . $$rand;
\t$$sock = $$function_name('127.0.0.1', 1234);
\treturn $$sock;""")
    function = T.substitute(multiple_irc_return_false = multiple_irc_return_false)
    return function;
