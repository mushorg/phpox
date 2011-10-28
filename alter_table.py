import sqlite3

class LogSQLite(object):
    
    def __init__(self):
        self.connection = sqlite3.connect("sandbox.db")
        self.alter()
        
    def alter(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                ALTER TABLE events ADD irc_nickserv TEXT,
                irc_notice TEXT, irc_privmsg TEXT""")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        
i = LogSQLite()
i.alter()
