import sqlite3

class LogSQLite(object):
    
    def __init__(self):
        self.connection = sqlite3.connect("sandbox.db")
        self.alter()
        
    def alter(self):
        self.cursor = self.connection.cursor()
        '''self.cursor.execute("""ALTER TABLE events ADD COLUMN 'irc_nickserv TEXT'""")
        self.cursor.execute("""ALTER TABLE events ADD COLUMN 'irc_notice TEXT'""")
        self.cursor.execute("""ALTER TABLE events ADD COLUMN 'irc_privmsg TEXT'""")'''
        self.cursor.execute("""ALTER TABLE events ADD COLUMN 'first_analysis TEXT'""")
        self.cursor.execute("""ALTER TABLE events ADD COLUMN 'last_analysis TEXT'""")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        
i = LogSQLite()
