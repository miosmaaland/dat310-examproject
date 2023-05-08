import sqlite3
from werkzeug.security import generate_password_hash

# Connect to database
conn = sqlite3.connect('recommendations.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL UNIQUE,
              password TEXT NOT NULL)'''
          )

# Insert sample data
password = generate_password_hash('Mio123')
users = [('Mio', password)]
c.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)

# Commit changes and close database connection
conn.commit()
conn.close()
