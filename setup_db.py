import sqlite3
from werkzeug.security import generate_password_hash

# Connect to database
conn = sqlite3.connect('recommendations.db')
c = conn.cursor()

# Create users table
c.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL UNIQUE,
              password TEXT NOT NULL)'''
          )

# Create series table
c.execute('''CREATE TABLE series
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              genre TEXT NOT NULL,
              platform TEXT NOT NULL)'''
          )

# Insert sample data
password = generate_password_hash('Mio123')
users = [('Mio', password)]
c.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)

series = [('Game of Thrones', 'Fantasy', 'HBO'),
          ('Breaking Bad', 'Drama', 'Netflix'),
          ('The Crown', 'Drama', 'Netflix'),
          ('Stranger Things', 'Horror', 'Netflix'),
          ('The Boys', 'Superhero', 'Amazon Prime'),
          ('Modern Family', 'Feel-good', 'Netflix'),
          ('How I Met Your Mother', 'Comedy', 'Disney +'),
          ('WestWorld', 'Sci-fi', 'HBO'),
          ('The Mandalorian', 'Comedy', 'Disney +'),
          ('Chernobyl', 'Drama', 'HBO'),
          ('The Big Bang Theory', 'Comedy', 'Netflix'),
          ('Reacher', 'Thriller', 'Amazon Prime')]
c.executemany('INSERT INTO series (name, genre, platform) VALUES (?, ?, ?)', series)

# Commit changes and close database connection
conn.commit()
conn.close()
