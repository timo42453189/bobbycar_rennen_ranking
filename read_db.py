import sqlite3

def read_from_db():
    con = sqlite3.connect('bobbycar.db')
    cur = con.cursor()
    res = cur.execute("SELECT * FROM ranking ORDER BY time ASC")
    x = res.fetchall()
    con.close()
    return x