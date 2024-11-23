from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
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

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_password",
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    create_users_table = """
    CREATE TABLE IF NOT EXISTS Users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        login_name VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        registration_date DATE DEFAULT CURRENT_DATE
    );
    """
    cursor.execute(create_users_table)

    create_tasks_table = """
    CREATE TABLE IF NOT EXISTS Tasks (
        task_id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(255) NOT NULL,
        assigned_user INT,
        start_date DATE DEFAULT CURRENT_DATE,
        due_date DATE,
        status VARCHAR(50) DEFAULT 'Pending',
        FOREIGN KEY (assigned_user) REFERENCES Users(user_id)
    );
    """
    cursor.execute(create_tasks_table)

    conn.commit()
    cursor.close()
    conn.close()

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
        cursor.execute('INSERT INTO Users (login_name, password, email) VALUES (%s, %s, %s)',
                       (login_name, password, email))
        conn.commit()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('index'))
    except mysql.connector.IntegrityError:
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

    cursor.execute('SELECT * FROM Users WHERE login_name = %s AND password = %s',
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