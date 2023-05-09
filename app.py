from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re
import jsonify

# Create the Flask app
app = Flask(__name__)
app.secret_key = 'my_secret_key'

# Setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# User model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Login page
# Index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        genre = request.form['genre']
        platform = request.form['platform']
        return redirect(url_for('search', genre=genre, platform=platform))
    else:
        return render_template('index.html')


# Login page
# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('search'))

    error = None
    if request.method == 'POST':
        # Check if user exists and password is correct
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('recommendations.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user is None or not check_password_hash(user[2], password):
            error = 'Invalid credentials.'
        else:
            user_obj = User(user[0])
            login_user(user_obj)
            return redirect(url_for('search'))

    return render_template('login.html', error=error)


# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('search'))

    error = None
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        password = request.form['password']

        # Check if the user already exists in the database
        conn = sqlite3.connect('recommendations.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            error = 'Username already taken.'
        elif len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Z]', password):
            error = 'Password must be at least 8 characters long and contain at least one uppercase letter and one number.'
        else:
            # Add the new user to the database
            password_hash = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
            conn.commit()

            # Log the new user in
            user_id = cursor.lastrowid
            user_obj = User(user_id)
            login_user(user_obj)
            return redirect(url_for('search'))

        conn.close()
    else:
        return render_template('register.html', error=error)

    return render_template('register.html', error=error)






# Search page
# Search page
@app.route('/search')
def search():
    # Get the values of the genre and platform parameters
    genre = request.args.get('genre', '')
    platform = request.args.get('platform', '')

    # Connect to database
    conn = sqlite3.connect('recommendations.db')
    c = conn.cursor()

    # Build the query based on the parameters
    query = 'SELECT * FROM series'
    if genre and platform:
        query += f" WHERE genre='{genre}' AND platform='{platform}'"
    elif genre:
        query += f" WHERE genre='{genre}'"
    elif platform:
        query += f" WHERE platform='{platform}'"

    # Execute the query and get the results
    c.execute(query)
    series = [{'title': row[1], 'genre': row[2], 'platform': row[3]} for row in c.fetchall()]

    # Close database connection
    conn.close()

    # Return the results as JSON if the request type is application/json, else render the template
    if request.is_json:
        return jsonify(series)
    else:
        return render_template('results.html', series=series)

@app.route('/series')
def get_series():
    # Get the selected genre and platform
    genre = request.args.get('genre', 'all')
    platform = request.args.get('platform', 'all')

    # Query the database based on selected options
    conn = sqlite3.connect('recommendations.db')
    cursor = conn.cursor()
    if genre == 'all' and platform == 'all':
        cursor.execute('SELECT * FROM series ORDER BY RANDOM() LIMIT 1')
    elif genre == 'all':
        cursor.execute('SELECT * FROM series WHERE platform = ? ORDER BY RANDOM() LIMIT 1', (platform,))
    elif platform == 'all':
        cursor.execute('SELECT * FROM series WHERE genre = ? ORDER BY RANDOM() LIMIT 1', (genre,))
    else:
        cursor.execute('SELECT * FROM series WHERE genre = ? AND platform = ? ORDER BY RANDOM() LIMIT 1', (genre, platform))

    series = cursor.fetchone()
    conn.close()

    if series is None:
        return jsonify(error='No series found.')

    #





if __name__ == '__main__':
    app.run(debug=True, port = 42373)
