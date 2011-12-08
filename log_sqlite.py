import sqlite3
from datetime import datetime

class LogSQLite(object):
    
    def __init__(self):
        self.connection = sqlite3.connect("sandbox.db")
        self.create()
    
    
    def create(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS 
                botnets(id INTEGER PRIMARY KEY,
                file_md5 TEXT,
                file_name TEXT,
                irc_addr INTEGER,
                irc_server_pwd TEXT,
                irc_nick TEXT,
                irc_user TEXT,
                irc_mode TEXT,
                irc_channel TEXT,
                irc_nickserv TEXT,
                irc_notice TEXT,
                irc_privmsg TEXT,
                first_analysis_date TEXT,
                last_analysis_date TEXT)
                """)
        self.connection.commit()
        self.cursor.close()
        
    def check_md5(self, botnet):
        self.cursor = self.connection.cursor()
        self.cursor.execute("""SELECT first_analysis_date FROM botnets WHERE file_md5 == ?""", botnet.file_md5)
        date = self.cursor.fetchone()
        self.cursor.close()
        return date
        
    def insert(self, botnet):
        date = self.check_md5(botnet)
        if date == "":
            botnet.first_analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            botnet.first_analysis_date = date
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                INSERT INTO botnets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (None, botnet.file_md5, botnet.file_name, botnet.irc_addr,
                 botnet.irc_server_pwd, botnet.irc_nick, botnet.irc_user,
                 botnet.irc_mode, ', '.join(botnet.irc_channel), repr(str(botnet.irc_nickserv)).replace("'", ""),
                 ', '.join(botnet.irc_notice), repr(str(botnet.irc_privmsg)).replace("'", ""),
                 botnet.first_analysis_date, botnet.last_analysis_date))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
