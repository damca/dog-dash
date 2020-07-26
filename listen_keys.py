import os
import time
import datetime
import keyboard


# get database connection
import sqlite3
from sqlite3 import Error


db_path = 'db/scat.sqlite'
def create_connection(db_path):
    conn = None
    conn = sqlite3.connect(db_path)
    print(sqlite3.version)
    return conn


sql_create_scat = """
                  CREATE TABLE IF NOT EXISTS scat (
                    id integer not null PRIMARY KEY,
                    time datetime NOT NULL,
                    key integer
                    );
                  """
def create_table(conn, sql):
    c = conn.cursor()
    c.execute(sql)


sql_insert = """
             INSERT INTO scat(time,key) VALUES(?,?)
             """
def insert_scat(conn, scat):
    c = conn.cursor()
    c.execute(sql_insert, scat)
    conn.commit()
    return c.lastrowid


conn = create_connection(db_path)
create_table(conn, sql_create_scat) # initialize table if not present

# transfer data from csv, if exists, then delete
import os
import pandas as pd
if os.path.exists('data/dog.csv'):
    pfmt = '%Y-%m-%d %H:%M:%S.%f'
    df = pd.read_csv('data/dog.csv')
    for ix, r in df.iterrows():
        dt = datetime.datetime.strptime(r['time'], pfmt)
        rid = insert_scat(conn, (dt, int(r['key'])))
        print('added new row:', rid, dt, r['key'])
    dfq = pd.read_sql_query("SELECT * from scat", conn)
    if dfq.drop(columns='id').shape == df.shape:
        print('csv and sql have same shape, deleting csv')
        os.remove('data/dog.csv')
    else:
        raise IndexError("csv and sql have different shapes")


global releaseListening, keepListening
keepListening = True

def key_press(key):
    print(key.name)
    if key.name == 'esc':
        # Stop listener
        keepListening = False
    now = datetime.datetime.now()
    if key.name in ['0', '1', '2']:
        insert_scat(conn, (now, int(key.name)))

keyboard.on_press(key_press)

# Collect events until released
def start():
    while keepListening:
        time.sleep(1)

