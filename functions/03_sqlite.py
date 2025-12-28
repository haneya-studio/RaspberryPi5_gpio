import sqlite3
import pandas as pd
from datetime import datetime

dbpath = './hoge_db.sqlite'
connection = sqlite3.connect(dbpath)
cursor = connection.cursor()

table = 'cds'

def add(value=0):
    try:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table} (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT NOT NULL,
                value INTEGER NOT NULL
            )
        ''')
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 現在時刻をISO 8601形式で取得
        cursor.execute('INSERT INTO cds (datetime, value) VALUES (?, ?)', (current_time, value))

        connection.commit()
        connection.close()
        # print("Record inserted successfully!")

    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])


def load():
    connection = sqlite3.connect(dbpath)
    df = pd.read_sql_query('SELECT * FROM cds', connection)
    print(df)
    connection.close()

if __name__ == "__main__":
    add()
    load()
