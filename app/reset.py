import sqlite3   #enable control of an sqlite database
import json

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

command = "DROP TABLE IF EXISTS users;" # delete table
c.execute(command)


command = "CREATE TABLE IF NOT EXISTS users (id TEXT, hidden_class_ids TEXT, group_class_ids TEXT);" # create table
c.execute(command)    # run SQL statement

with open('client_secret.json') as json_file:
    data = json.load(json_file)
    c.execute("INSERT INTO users VALUES(?, ?, ?)", ('me', '', ''))


db.commit()
db.close()
