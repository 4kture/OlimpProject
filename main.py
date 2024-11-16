from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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

get_db_connection()
init_db()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)