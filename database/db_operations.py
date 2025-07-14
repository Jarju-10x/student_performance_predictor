import sqlite3
from typing import List, Optional
from .models import User, Student
#import pandas as pd


def initialize_database():
    """Initialize the database with required tables"""
     
    conn = sqlite3.connect('student_performance.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')
    
    # Create students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT,
        age INTEGER,
        location TEXT,
        famsize TEXT,
        pstatus TEXT,
        medu INTEGER,
        fedu INTEGER,
        traveltime INTEGER,
        studytime INTEGER,
        failures INTEGER,
        schoolsup TEXT,
        famsup TEXT,
        paid TEXT,
 
 activities TEXT,
        nursery TEXT,
        higher TEXT,
        internet TEXT,
        famrel INTEGER,
        freetime INTEGER,
        health INTEGER,
        absences INTEGER,
        score INTEGER,
        performance_category TEXT
    )
    ''')
    
    # Insert default admin user if not exists
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                      ('admin', 'admin123', 'admin'))
    except sqlite3.IntegrityError:
        pass  # User already exists
    
    conn.commit()
    conn.close()

def get_user(username: str) -> Optional[User]:
    """Retrieve a user by username"""
    conn = sqlite3.connect('student_performance.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(*user_data)
    return None

def get_all_students() -> List[Student]:
    """Retrieve all students from the database"""
    conn = sqlite3.connect('student_performance.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students")
    students = [Student(*row) for row in cursor.fetchall()]
    conn.close()
    
    return students

# Add other database operations as needed...


if __name__ == '__main__':
    std_count = get_all_students()
    print(len(std_count))
