import sqlite3

# Create a new database file
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create the users table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("✅ Fresh users.db created successfully.")
