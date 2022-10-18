import sqlite3
from pathlib import Path
import datetime


dbname = "badape.db"
dbfolder = "db/"
badape_dict = {}

comments_me_count = 0
comments_processed_count = 0
goodbot_count = 0
badbot_count = 0
deleted_count = 0


# This makes the database folder if it doesn't exist
Path(dbfolder).mkdir(parents=True, exist_ok=True)


#date   How many comments I've made     how many comments I've processed        How many good bots      How many bad bots       How many deleted comments
def init_sqlite():
    conn = sqlite3.connect(dbfolder + dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE stats (date date, Comments_Made int, Comments_Read int, Good_Bot int, Bad_Bot int, Deleted int)''')

def sqlite_connect():
    global conn
    conn = sqlite3.connect(dbfolder + dbname, check_same_thread=False)

def sqlite_load_all():
    sqlite_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM stats ORDER BY date DESC LIMIT 1')
    rows = c.fetchall()
    conn.close()
    return rows

def badape_load():
    global comments_me_count
    global comments_processed_count
    global goodbot_count
    global badbot_count
    global deleted_count
    global badape_dict
    if bool(badape_dict):
        badape_dict.clear()
    for row in sqlite_load_all():
        badape_dict=(row[0],row[1], row[2], row[3], row[4],row[5])
    comments_me_count = badape_dict[1]
    comments_processed_count = badape_dict[2]
    goodbot_count = badape_dict[3]
    badbot_count = badape_dict[4]
    deleted_count = badape_dict[5]


def sqlite_write(comments_made,comments_read,good,bad,deleted):
    sqlite_connect()
    c = conn.cursor()
    x = datetime.datetime.now()
    q = [(x), (comments_made), (comments_read), (good), (bad), (deleted)]
    c.execute('''INSERT INTO stats('date','Comments_Made','Comments_Read','Good_Bot','Bad_Bot','Deleted') VALUES(?,?,?,?,?,?)''', q)
    conn.commit()
    conn.close()


try:
    init_sqlite()
except sqlite3.OperationalError:
    pass