"""
It's used to extend the database, sandbox.db with text COLUMN 
"irc_nickserv", "irc_notice", "irc_privmsg", and "first_analysis."
"""

import sqlite3

"""
class LogSQLite with member function ¡§alter¡¨ which will add columns to 
the database , "sandbox.db" , and declare an instance of class LogSQLite.
"""
class LogSQLite(object):
    
    def __init__(self):
        self.connection = sqlite3.connect("sandbox.db")
        self.alter()
        
    def alter(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute("""ALTER TABLE events ADD COLUMN 'irc_nickserv TEXT'""")
        self.cursor.execute("""ALTER TABLE events ADD COLUMN 'irc_notice TEXT'""")
        self.cursor.execute("""ALTER TABLE events ADD COLUMN 'irc_privmsg TEXT'""")
        self.cursor.execute("""ALTER TABLE events ADD COLUMN 'first_analysis TEXT'""")
        self.cursor.execute("""ALTER TABLE events ADD COLUMN 'last_analysis TEXT'""")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        
i = LogSQLite()
