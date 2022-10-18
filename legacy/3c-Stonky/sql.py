import sqlite3
from pathlib import Path

dbname = "stonky.db"
dbfolder = "db/"

Path(dbfolder).mkdir(parents=True, exist_ok=True)

# Initial connection to the database
def sqlite_connect():
    global conn
    conn = sqlite3.connect(dbfolder + dbname, check_same_thread=False)

# Load all data from the database
def sqlite_load_all():
    sqlite_connect()
    c = conn.cursor()
    c.execute('SELECT userid FROM flairmods')
    rows = c.fetchall()
    c.execute('SELECT id FROM flaircomments')
    rows2 = c.fetchall()
    conn.close()
    return rows, rows2

# Create the database file and table if they don't exist
def init_sqlite():
    conn = sqlite3.connect(dbfolder + dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE flairmods (userid text, promoter text, id text)''')
    c.execute('''CREATE TABLE flaircomments (userid text, id text, time timestamp)''')
    c.execute('''CREATE TABLE neurotic (postID text, tag text)''')
    c.execute('''CREATE TABLE mods (modName text, tag text)''')

#################
# Flair Functions
#################
def flairmod_write(userid, promoter, id):
    sqlite_connect()
    c = conn.cursor()
    q = [(userid), (promoter),(id)]
    c.execute('''INSERT INTO flairmods ('userid','promoter', 'id') VALUES(?,?,?)''', q)
    conn.commit()
    conn.close()

def flaircomment_write(userid, id, timestamp):
    sqlite_connect()
    c = conn.cursor()
    q = [(userid), (timestamp),(id)]
    c.execute('''INSERT INTO flaircomments ('userid', 'id', 'time') VALUES(?,?,?)''', q)
    conn.commit()
    conn.close()

# Delete a flairmod
def flairmod_remove(flairmod):
    sqlite_connect()
    sql = 'DELETE FROM flairmods WHERE userid=?'
    c = conn.cursor()
    c.execute(sql, (flairmod,))
    conn.commit()
    conn.close()

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

###########
# Mod Stuff
###########

def modReader_sql():        # Pull recorded mod data
    sqlite_connect()
    c = conn.cursor()
    c.execute("SELECT modName FROM mods")
    rows = c.fetchall()
    conn.close()
    return rows


def modWriter_sql(modName):
    sqlite_connect()
    c = conn.cursor()
    q = [(str(modName)), (None)]
    c.execute('''INSERT INTO modName ('modName', 'tag') VALUES(?,?)''', q)
    conn.commit()
    conn.close()


try:
    init_sqlite()
except sqlite3.OperationalError:
    pass