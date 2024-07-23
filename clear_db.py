import sqlite3

con = sqlite3.connect('bobbycar.db')
cur = con.cursor()
cur.execute("DELETE FROM ranking")
con.commit()
con.close()