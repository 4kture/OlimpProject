from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('Main.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        login_name TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        registration_date DATE DEFAULT CURRENT_DATE
    )
    ''')

    # база данных для работы с данными (будет позже)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        assigned_user INTEGER,
        start_date DATE DEFAULT CURRENT_DATE,
        due_date DATE,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (assigned_user) REFERENCES Users(user_id)
    )
    ''')

    conn.commit()
    conn.close()

init_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    tasks = []

    if request.method == 'POST':
        if 'register' in request.form:
            login_name = request.form['login_name']
            password = request.form['password']
            email = request.form['email']

            conn = sqlite3.connect('Main.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Users (login_name, password, email)
                VALUES (?, ?, ?)
            ''', (login_name, password, email))
            conn.commit()
            conn.close()

            message = 'Registration successful!'

        elif 'login' in request.form:
            login_name = request.form['login_name']
            password = request.form['password']

            conn = sqlite3.connect('Main.db')
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM Users WHERE login_name = ? AND password = ?
            ''', (login_name, password))
            user = cursor.fetchone()
            conn.close()

    return render_template('index.html', tasks=tasks, message=message)

if __name__ == '__main__':
    app.run(debug=True)