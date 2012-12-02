# Copyright (C) 2012  Lukas Rist
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

import sqlite3


class LogSQLite(object):
    """
    class LogSQLite with member function alter which will add columns to the database ,
    "sandbox.db" , and declare an instance of class LogSQLite.
    """
    def __init__(self):
        self.connection = sqlite3.connect("sandbox.db")
        self.alter()

    def alter(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute("""ALTER TABLE botnets ADD COLUMN 'irc_nickserv TEXT'""")
        self.cursor.execute("""ALTER TABLE botnets ADD COLUMN 'irc_notice TEXT'""")
        self.cursor.execute("""ALTER TABLE botnets ADD COLUMN 'irc_privmsg TEXT'""")
        self.cursor.execute("""ALTER TABLE botnets ADD COLUMN 'first_analysis TEXT'""")
        self.cursor.execute("""ALTER TABLE botnets ADD COLUMN 'last_analysis TEXT'""")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

i = LogSQLite()
