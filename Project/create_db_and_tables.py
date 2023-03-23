import sqlite3
import os

def create_database():
    # Connect to the database
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()


    # Create the books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT,
            copies INTEGER
        )
    """)

    # Create the students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)

    # Create the borrowed table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowed (
            book_id INTEGER,
            student_id INTEGER,
            borrow_date TIMESTAMP
        )
    """)



    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

def remove_database():
    os.remove('library.db')