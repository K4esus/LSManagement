import sqlite3
import csv
"""
Drops the feldaten table and recreates it with the mockdata
"""

CONNECTION = sqlite3.connect("main.db")
CONNECTION.execute("DROP TABLE IF EXISTS felddaten")
CONNECTION.commit()
CONNECTION.execute(
            "CREATE TABLE IF NOT EXISTS felddaten "
            "(fieldnumber INTEGER PRIMARY KEY, crop TEXT,precrop TEXT,cycle TEXT,lime TEXT,"
            "fertilizer TEXT,plow TEXT,roll TEXT,status TEXT,fieldsize REAL)"
        )
CONNECTION.commit()
with open("../testdata/Mockdata.csv") as f:
    for index, row in enumerate(csv.reader(f)):
        if index > 1:
            print(row)
            CONNECTION.execute("INSERT INTO felddaten VALUES (?,?,?,?,?,?,?,?,?,?)", row)
CONNECTION.commit()
