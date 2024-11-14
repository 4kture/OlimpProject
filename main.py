import sqlite3

conn = sqlite3.connect('Main.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    login_name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    registration_date DATE DEFAULT CURRENT_DATE
)
''')

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