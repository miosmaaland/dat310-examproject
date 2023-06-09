import sqlite3
from werkzeug.security import generate_password_hash

# Connect to the database
conn = sqlite3.connect('recommendations.db')
c = conn.cursor()

# Create the users table
# Create the users table
# Create the users table
# Create the users table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        profile_image TEXT DEFAULT ''
    )
''')


# Create the series table
c.execute('''CREATE TABLE IF NOT EXISTS series
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              genre TEXT NOT NULL,
              platform TEXT NOT NULL)'''
          )


# Create the searches table
c.execute('''
    CREATE TABLE IF NOT EXISTS searches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        genre TEXT,
        platform TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')


# Insert sample data
password = generate_password_hash('Mio123')
users = [('Mio', password)]
c.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)

series = [
    # Action
    ('Game of Thrones', 'action', 'hbo'),
    ('Stranger Things', 'action', 'netflix'),
    ('The Boys', 'action', 'amazon'),

    # comedy
    ('the office', 'comedy', 'netflix'),
    ('brooklyn nine-nine', 'comedy', 'hulu'),
    ('how i met your mother', 'comedy', 'disney+'),

    # drama
    ('breaking bad', 'drama', 'netflix'),
    ('the crown', 'drama', 'netflix'),
    ('chernobyl', 'drama', 'hbo'),

    # romance
    ('friends', 'romance', 'netflix'),
    ('outlander', 'romance', 'starz'),

    # anime
    ('attack on titan', 'anime', 'netflix'),
    ('one piece', 'anime', 'hulu'),

    # thriller
    ('money heist', 'thriller', 'netflix'),
    ('true detective', 'thriller', 'hbo'),

    # additional series
    ('modern family', 'comedy', 'netflix'),
    ('westworld', 'sci-fi', 'hbo'),
    ('the mandalorian', 'sci-fi', 'disney+'),
    ('the witcher', 'fantasy', 'netflix'),
    ('the handmaid\'s tale', 'drama', 'hulu'),
    ('the marvelous mrs. maisel', 'comedy', 'amazon prime'),
    ('breaking bad', 'crime', 'amc'),
    ('stranger things', 'horror', 'netflix'),
    ('friends', 'comedy', 'nbc'),
    ('the big bang theory', 'comedy', 'netflix')
]

c.executemany('INSERT INTO series (name, genre, platform) VALUES (?, ?, ?)', series)

# Commit changes and close the database connection
conn.commit()
conn.close()