import os
import sqlite3
import pandas as pd

dbpath = './hoge_db.sqlite'
connection = sqlite3.connect(dbpath)

df = pd.read_sql_query('SELECT * FROM cds', connection)
print(df)