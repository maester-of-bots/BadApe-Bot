import sqlite3
from pathlib import Path

dbname = "stonky.db"
dbfolder = "db/"

Path(dbfolder).mkdir(parents=True, exist_ok=True)

# Initial connection to the database
def sqlite_connect():
    global conn
    conn = sqlite3.connect(dbfolder + dbname, check_same_thread=False)


# Create the database file and table if they don't exist
def init_sqlite():
    conn = sqlite3.connect(dbfolder + dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE neurotic (postID text, tag text)''')


####################
# Neurotic Functions
####################

# Write to the database for flagging posts as a certain denomination
# Requires the post ID, and what it is; EG pro GME, anti GME, etc
def Neurotic_Write(postID, tag):
    sqlite_connect()
    c = conn.cursor()
    q = [(str(postID)), (tag)]
    c.execute('''INSERT INTO neurotic ('postID', 'tag') VALUES(?,?)''', q)
    conn.commit()
    conn.close()

def Neurotic_Read(tag):
    sqlite_connect()
    c = conn.cursor()
    c.execute("SELECT postID FROM neurotic WHERE tag = '%s'" % tag)
    rows = c.fetchall()
    conn.close()
    return rows


try:
    init_sqlite()
except sqlite3.OperationalError:
    pass
