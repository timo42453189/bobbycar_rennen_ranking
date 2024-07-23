import sqlite3


def write_to_db(name, time):
    con = sqlite3.connect('bobbycar.db')
    cur = con.cursor()
    cur.execute("INSERT INTO ranking VALUES (?, ?)", (name, time))
    con.commit()
    con.close()

def delete_item(name):
    con = sqlite3.connect('bobbycar.db')
    cur = con.cursor()
    cur.execute("DELETE FROM ranking WHERE name = ?", (name,))
    con.commit()
    con.close()