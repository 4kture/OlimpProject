from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)

def by_fourture():
    print("\033[36m------------------------------------------------------------\033[0m")
    print("\033[36m _____                      _____                    \033[0m")
    print("\033[36m|  ___|  ___   _   _  _ __ |_   _| _   _  _ __   ___ \033[0m")
    print("\033[36m| |_    / _ \ | | | || '__|  | |  | | | || '__| / _ \\\033[0m")
    print("\033[36m|  _|  | (_) || |_| || |     | |  | |_| || |   |  __/\033[0m")
    print("\033[36m|_|     \___/  \__,_||_|     |_|   \__,_||_|    \___|\033[0m")
    print("\033[36m------------------------------------------------------------\033[0m")

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

def get_db_connection():
    conn = sqlite3.connect('Main.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/task-manager')
def task_manager():
    return render_template('task-manager.html')

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
        return redirect(url_for('task_manager'))
    else:
        flash('Неверный логин или пароль.', 'error')
        return redirect(url_for('index'))

@app.route('/exit', methods=['POST'])
def a_exit():
    session.pop('user_id', None)
    flash('Выход успешен!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    by_fourture()
    app.run(debug=True)