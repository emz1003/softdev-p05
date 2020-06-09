import sqlite3 #enable control of an sqlite database
import os

dirname = os.path.dirname(__file__) or '.'
DB_FILE =  dirname + '/../' + 'data.db'

def togglehide(userid, classid):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    output = c.execute("SELECT hidden_class_ids FROM users WHERE id = (?)", (userid,)).fetchall()
    if len(output) == 0: # user not in db yet
        c.execute(
        """
            INSERT INTO users
            VALUES(?, ?, ?)
        """, (userid, classid, ""))

    else:
        classids = output[0][0]
        print(classids)
        if classids.find(classid) == -1:
            classids += (" " + classid)
        else:
            classids = classids.replace(classid, "")

        c.execute(
        """
            UPDATE users
            SET hidden_class_ids = (?)
            WHERE id = (?)
        """, (classids, userid))

    db.commit()
    db.close()

def get_hidden_classes(userid):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    output = c.execute("SELECT hidden_class_ids FROM users WHERE id = (?)", (userid,)).fetchall()
    db.close()

    if len(output) == 0:
        return ""

    else:
        return output[0][0]
