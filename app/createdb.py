import sqlite3 #enable control of an sqlite database

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

command = "CREATE TABLE users (id TEXT, hidden_class_ids TEXT, group_class_ids TEXT);" # create table
c.execute(command)    # run SQL statement

db.commit()
db.close()
