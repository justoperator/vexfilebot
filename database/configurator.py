import sqlite3

conn = sqlite3.connect('database/main.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY,
          username VARCHAR(50),
          lang VARCHAR(4)
          )
''')

conn.commit()
conn.close()