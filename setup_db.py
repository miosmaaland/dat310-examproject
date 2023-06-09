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
    ('Game of Thrones', 'Action', 'HBO'),
    ('Stranger Things', 'Action', 'Netflix'),
    ('The Boys', 'Action', 'Amazon Prime'),

    # Comedy
    ('The Office', 'Comedy', 'Netflix'),
    ('Brooklyn Nine-Nine', 'Comedy', 'Hulu'),
    ('How I Met Your Mother', 'Comedy', 'Disney+'),

    # Drama
    ('Breaking Bad', 'Drama', 'Netflix'),
    ('The Crown', 'Drama', 'Netflix'),
    ('Chernobyl', 'Drama', 'HBO'),

    # Romance
    ('Friends', 'Romance', 'Netflix'),
    ('Outlander', 'Romance', 'Starz'),

    # Anime
    ('Attack on Titan', 'Anime', 'Netflix'),
    ('One Piece', 'Anime', 'Hulu'),

    # Thriller
    ('Money Heist', 'Thriller', 'Netflix'),
    ('True Detective', 'Thriller', 'HBO'),

    # Additional series
    ('Modern Family', 'Comedy', 'Netflix'),
    ('Westworld', 'Sci-Fi', 'HBO'),
    ('The Mandalorian', 'Sci-Fi', 'Disney+'),
    ('The Witcher', 'Fantasy', 'Netflix'),
    ('The Handmaid\'s Tale', 'Drama', 'Hulu'),
    ('The Marvelous Mrs. Maisel', 'Comedy', 'Amazon Prime'),
    ('Breaking Bad', 'Crime', 'AMC'),
    ('Stranger Things', 'Horror', 'Netflix'),
    ('Friends', 'Comedy', 'NBC'),
    ('The Big Bang Theory', 'Comedy', 'Netflix'),
]

c.executemany('INSERT INTO series (name, genre, platform) VALUES (?, ?, ?)', series)

# Commit changes and close the database connection
conn.commit()
conn.close()
