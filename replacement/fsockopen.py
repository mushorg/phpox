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

from php import utils as php_utils
from string import Template


def call():
    utils = php_utils.UtilFunctions()
    multiple_irc_return_false = utils.get_symbol("multiple_irc_return_false")
    template = Template(
        """\techo "\\nADDR " . $$hostname . ':' . $$port . "\\n";
\t$$multiple_irc_return_false = "${multiple_irc_return_false}";
\tif($$multiple_irc_return_false()){
\t\tif(rand(0,1) == 0){
\t\t\techo "\\nMULTIPLE IRC Server return FALSE\\n";
\t\t\treturn FALSE;
\t\t}
\t}
\t$$function_name = "fsockopen" . "_" . $$rand;
\t$$sock = $$function_name('127.0.0.1', 1234);
\treturn $$sock;"""
    )
    function = template.substitute(multiple_irc_return_false=multiple_irc_return_false)
    return function
