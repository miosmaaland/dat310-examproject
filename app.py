from flask import Flask, jsonify, request, session, redirect, url_for
import os
import json

app = Flask(__name__)
app.secret_key = 'super secret key'

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CONTACTS_FILE = os.path.join(DATA_DIR, "contacts.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")


def create_file_if_not_exists(filename):
    if not os.path.exists(filename):
        try:
            with open(filename, "w") as f:
                json.dump({}, f)
        except:
            print(f"Error creating file {filename}")
    else:
        print(f"File {filename} already exists")


def read_json_file(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def initialize_files():
    global users, address_book
    users = read_json_file(USERS_FILE)
    address_book = read_json_file(CONTACTS_FILE)


initialize_files()


@app.route('/', methods=['GET'])
def home():
    if session.get('username'):
        username = session['username']
        if username not in address_book:
            return f"Welcome, {username}!<br><br>You don't have an address book yet.<br><br><a href='/logout'>Logout</a>"
        else:
            return f"Welcome, {username}!<br><br>Your address book:<br>{json.dumps(address_book[username])}<br><br><a href='/logout'>Logout</a>"
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid username or password"
    else:
        return '''
               <form method="post">
                <h2>Login</h2>
                <p>Username: <input type="text" name="username"></p>
                <p>Password: <input type="password" name="password"></p>
                <p><input type="submit" value="Login"></p>
               </form>
               '''


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/address_book', methods=['GET'])
def get_address_book():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if username not in address_book:
        return "You don't have an address book yet!"
    return jsonify(address_book[username])


@app.route('/address_book', methods=['POST'])
def add_contact():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if username not in address_book:
        address_book[username] = {}
    new_contact = request.get_json()
    for name, address in new_contact.items():
        address_book[username][name] = address
    with open(CONTACTS_FILE, "w") as f:
        json.dump(address_book, f)
    return "Contact added successfully!"


@app.route('/address_book', methods=['PUT'])
def edit_contact():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if username not in address_book:
        return "You don't have an address book yet!"
    updated_contact = request.get_json()
    for name, address in updated_contact.items():
        if name in address_book[username]:
            address_book[username][name] = address
        else:
            return "Contact not found!"
    with open(CONTACTS_FILE, "w") as f:
        json.dump(address_book, f)
    return "Contact updated successfully!"


@app.route('/address_book', methods=['DELETE'])
def delete_contact():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if username not in address_book:
        return "You don't have an address book yet!"
    contact_to_delete = request.get_json()
    for name in contact_to_delete:
        if name in address_book[username]:
            del address_book[username][name]
        else:
            return "Contact not found!"
    with open(CONTACTS_FILE, "w") as f:
        json.dump(address_book, f)
    return "Contact deleted successfully!"

if __name__ == '__main__':
    app.run()