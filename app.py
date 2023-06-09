from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re


app = Flask(__name__)
app.secret_key = 'my_secret_key'


app.config['SESSION_COOKIE_SECURE'] = False

# Setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# User model
class User(UserMixin):
    def __init__(self, id, username, profile_image=None):
        self.id = id
        self.username = username
        self.profile_image = profile_image


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('recommendations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])  
    return None



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    error = None
    if request.method == 'POST':
        # Check if user exists and password is correct
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('recommendations.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data is None or not check_password_hash(user_data[2], password):
            error = 'Invalid credentials.'
        else:
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            return redirect(url_for('profile'))

    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('register'))

    error = None
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        password = request.form['password']

       
        conn = sqlite3.connect('recommendations.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            error = 'Username already taken.'
        elif len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Z]', password):
            error = 'Password must be at least 8 characters long and contain at least one uppercase letter and one number.'
        else:
           
            password_hash = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password, profile_image) VALUES (?, ?, ?)', (username, password_hash, ''))
            conn.commit()

           
            user_id = cursor.lastrowid
            registered_user = User(user_id, username)  # Create a new User object
            login_user(registered_user)


            conn.close()  

            return redirect(url_for('profile'))

        conn.close()

    return render_template('register.html', error=error)



@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        
        if 'profile_image' in request.files:
            profile_image = request.files['profile_image']
            if profile_image.filename != '':
                
                profile_image.save('static/profile_images/' + current_user.username + '.jpg')
                flash('Profile image uploaded successfully.')

    return render_template('profile.html')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        genre = request.form.get('genre')
        platform = request.form.get('platform')
        user_id = current_user.id

        conn = sqlite3.connect('recommendations.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO searches (user_id, genre, platform) VALUES (?, ?, ?)', (user_id, genre, platform))
        conn.commit()
        conn.close()

        conn = sqlite3.connect('recommendations.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM series WHERE genre = ? AND platform = ?', (genre, platform))
        series = cursor.fetchall()
        conn.close()

        return render_template('results.html', genre=genre, platform=platform, series=series)

    return redirect(url_for('search'))

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        genre = request.form.get('genre')
        platform = request.form.get('platform')
        user_id = None
        if current_user.is_authenticated:
            user_id = current_user.id

        conn = sqlite3.connect('recommendations.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO searches (user_id, genre, platform) VALUES (?, ?, ?)', (user_id, genre, platform))
        conn.commit()
        conn.close()

        conn = sqlite3.connect('recommendations.db')
        c = conn.cursor()
        if genre == 'all' and platform == 'all':
            c.execute('SELECT * FROM series')
        elif genre == 'all':
            c.execute('SELECT * FROM series WHERE platform=?', (platform,))
        elif platform == 'all':
            c.execute('SELECT * FROM series WHERE genre=?', (genre,))
        else:
            c.execute('SELECT * FROM series WHERE genre=? AND platform=?', (genre, platform))
        series = c.fetchall()
        conn.close()
        return render_template('results.html', genre=genre, platform=platform, series=series)

    # Method not allowed for GET requests
    return redirect(url_for('search'))


if __name__ == '__main__':
    app.run(debug=True, port=56792)