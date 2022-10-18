import sqlite3
from pathlib import Path
from datetime import *

dbname = "anti_drs.db"
dbfolder = "db/"

Path(dbfolder).mkdir(parents=True, exist_ok=True)

# SQL stuff
def sqlite_connect():
    global conn
    conn = sqlite3.connect(dbfolder + dbname, check_same_thread=False)
    conn.row_factory = lambda cursor, row: row[0]

def init_sqlite():
    conn = sqlite3.connect(dbfolder + dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE removed (date timestamp, username text, removed int )''')
    c.execute('''CREATE TABLE comments (id text)''')

def getCharges(username):
    sqlite_connect()
    c = conn.cursor()
    q = [(username)]
    c.execute("""SELECT removed FROM removed WHERE username=?""",q)
    result = c.fetchall()
    if result == []:
        return 0, 0
    else:
        return sum(result), len(result)

def writeCharges(username,count):
    command = '''INSERT INTO removed('date','username','removed') VALUES(?,?,?)'''
    q = [(datetime.utcnow()),(username), (count)]
    sqlite_connect()
    c = conn.cursor()
    c.execute(command, q)
    conn.commit()
    conn.close()

def getComments():
    sqlite_connect()
    c = conn.cursor()
    c.execute("""SELECT id FROM comments""")
    result = c.fetchall()
    return result

def writeComment(id):
    with open('log.txt', 'a') as file:
        file.write(id+"\n")
    sqlite_connect()
    c = conn.cursor()
    q = [(id)]
    c.execute('''INSERT INTO comments('id') VALUES(?)''', q)
    conn.commit()
    conn.close()


try:
    init_sqlite()
except:
    pass
