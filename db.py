import sqlite3

conn=sqlite3.connect("database.db")

conn.execute("CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,address TEXT,city TEXT,pin TEXT)")
print("table created")
conn.close()