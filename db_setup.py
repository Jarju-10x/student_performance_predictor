# db_setup.py
import sqlite3

def init_db():
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()

    # Create Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT,
            semester INTEGER,
            marks REAL,
            attendance REAL,
            participation REAL
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    init_db()

