from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_db_connection():
    conn = sqlite3.connect('Main.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect('Main.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        login_name TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        registration_date DATE DEFAULT CURRENT_DATE
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        assigned_user INTEGER,
        start_date DATE DEFAULT CURRENT_DATE,
        due_date DATE,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (assigned_user) REFERENCES Users(user_id)
    )''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    login_name = request.form['login_name']
    password = request.form['password']
    email = request.form['email']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO Users (login_name, password, email) VALUES (?, ?, ?)',
                       (login_name, password, email))
        conn.commit()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('index'))
    except sqlite3.IntegrityError:
        flash('Пользователь с таким логином или почтой уже существует!', 'error')
        return redirect(url_for('index'))
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    login_name = request.form['login_name']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Users WHERE login_name = ? AND password = ?',
                   (login_name, password))
    user = cursor.fetchone()

    if user:
        flash('Вход успешен!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Неверный логин или пароль.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)