from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import os

app = Flask(__name__, template_folder='templates')
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        date_created TEXT DEFAULT CURRENT_TIMESTAMP
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

@app.route('/task-manager', methods=['GET', 'POST'])
def task_manager():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        cursor.execute("INSERT INTO Tasks (title, description) VALUES (?, ?)",
                       (title, description))
        conn.commit()
        flash('Задача добавлена!', 'success')

    cursor.execute("SELECT * FROM Tasks")
    tasks = cursor.fetchall()
    conn.close()

    return render_template('task-manager.html', tasks=tasks)

@app.route('/delete-task/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    flash('Задача удалена!', 'success')
    return redirect(url_for('task_manager'))

@app.route('/edit-task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cursor.execute("UPDATE Tasks SET title = ?, description = ? WHERE id = ?",
                       (title, description, task_id))
        conn.commit()
        conn.close()
        flash('Задача обновлена!', 'success')
        return redirect(url_for('task_manager'))

    cursor.execute("SELECT * FROM Tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()

    return render_template('edit-task.html', task=task)

if __name__ == '__main__':
    init_db()
    by_fourture()
    app.run(debug=True)