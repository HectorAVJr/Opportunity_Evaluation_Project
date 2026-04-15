import sqlite3

DB_NAME = "database.db"

def get_db_connection():
    return sqlite3.connect(DB_NAME)


def init_db():

    print("Initializing database...")

    conn = get_db_connection()
    cursor = conn.cursor()

    # models table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS models (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    # criteria table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS criteria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id INTEGER,
        field_name TEXT,
        weight REAL,
        min REAL,
        max REAL
    )
    """)

    # derived_fields table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS derived_fields (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id INTEGER,
        name TEXT,
        formula TEXT
    )
    """)
    
     # opportunities table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id INTEGER,
        data TEXT,
        score REAL,
        decision TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Databased initialized successfully.")