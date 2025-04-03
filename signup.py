from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to execute SQL queries
def execute_query(query, args=()):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    conn.close()

# Sign-Up Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        try:
            execute_query('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
            flash('Sign up successful! Please sign in.', 'success')
            return redirect(url_for('signin'))
        except sqlite3.IntegrityError:
            flash('Email already exists. Please use another.', 'error')
            return redirect(url_for('signup'))
    return render_template('signup.html')

# Sign-In Route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        if row and check_password_hash(row[0], password):
            flash('Sign in successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('signin'))
    return render_template('signin.html')

# Home Route
@app.route('/')
def home():
    return '<h2>Welcome to the Home Page</h2>'

if __name__ == '__main__':
    app.run(debug=True)

