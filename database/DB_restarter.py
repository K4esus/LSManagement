import sqlite3
import csv
from werkzeug.security import generate_password_hash, check_password_hash
"""
Drops the feldaten table and recreates it with the mockdata
"""

CONNECTION = sqlite3.connect("main.db")
# drops all tables
#CONNECTION.execute("DROP TABLE IF EXISTS felddaten")
CONNECTION.execute("DROP TABLE IF EXISTS user")

# adds user and felddaten table
"""
CONNECTION.execute(
            "CREATE TABLE IF NOT EXISTS felddaten "
            "(fieldnumber INTEGER PRIMARY KEY, crop TEXT,precrop TEXT,cycle TEXT,lime TEXT,"
            "fertilizer TEXT,plow TEXT,roll TEXT,status TEXT,fieldsize REAL)"
        )

CONNECTION.execute("CREATE TABLE IF NOT EXISTS user "
                   "(username TEXT PRIMARY KEY, password_hash TEXT, admin BOOL)")

# fills felddaten with test data
with open("../testdata/Mockdata2.csv") as f:
    for index, row in enumerate(csv.reader(f)):
        if index > 1:
            print(row)
            CONNECTION.execute("INSERT INTO felddaten VALUES (?,?,?,?,?,?,?,?,?,?)", row)
"""

CONNECTION.execute("CREATE TABLE IF NOT EXISTS user "
                   "(username TEXT PRIMARY KEY, password_hash TEXT, admin BOOL)")
username = "Nig"
password = "LSMANAGEMENT"
admin = True
password_hash = generate_password_hash(password)
CONNECTION.execute("INSERT INTO user VALUES (?, ?, ?)", (username, password_hash, admin))
CONNECTION.commit()
