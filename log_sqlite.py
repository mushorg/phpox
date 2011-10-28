import sqlite3

class LogSQLite(object):
    
    def __init__(self):
        self.connection = sqlite3.connect("sandbox.db")
        self.create()
        
    def create(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS 
                events(id INTEGER PRIMARY KEY, analysis_date TEXT, file_md5 TEXT, 
                file_name TEXT, irc_addr INTEGER, irc_server_pwd TEXT, irc_nick TEXT,
                irc_user TEXT, irc_mode TEXT, irc_channel TEXT, irc_nickserv TEXT,
                irc_notice TEXT, irc_privmsg TEXT)""")
        self.connection.commit()
        self.cursor.close()
        
    def insert(self, botnet):
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (None, botnet.analysis_date, botnet.file_md5, botnet.file_name, 
                 botnet.irc_addr, botnet.irc_server_pwd, botnet.irc_nick,
                 botnet.irc_user, botnet.irc_mode, ', '.join(botnet.irc_channel),
                 botnet.irc_nickserv, ', '.join(botnet.irc_notice), ', '.join(botnet.irc_privmsg)))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()