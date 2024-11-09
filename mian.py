import os
import psycopg2
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash

# Load environment variables from .env file

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_HOST = "postgres"
DB_USER = "myuser"
DB_PASSWORD = "mysecretpassword"
DB_NAME = "mydatabase"
PORT=5432

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=PORT
    )
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        if check_user_credentials(email, password):
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('registration.html')

def check_user_credentials(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Query for user credentials
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            # Check password hash
            return check_password_hash(user[0], password)
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
