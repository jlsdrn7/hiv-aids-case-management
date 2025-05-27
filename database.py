import sqlite3

DB_NAME = "hiv_cases.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            diagnosis_date TEXT NOT NULL,
            contact_info TEXT NOT NULL,
            case_severity TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "1234"))

    conn.commit()
    conn.close()

def insert_case(full_name, diagnosis_date, contact_info, case_severity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cases (full_name, diagnosis_date, contact_info, case_severity)
        VALUES (?, ?, ?, ?)
    """, (full_name, diagnosis_date, contact_info, case_severity))
    conn.commit()
    conn.close()

def fetch_all_cases():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, full_name, diagnosis_date, contact_info, case_severity
        FROM cases
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_case(case_id, full_name, diagnosis_date, contact_info, case_severity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cases
        SET full_name = ?, diagnosis_date = ?, contact_info = ?, case_severity = ?
        WHERE id = ?
    """, (full_name, diagnosis_date, contact_info, case_severity, case_id))
    conn.commit()
    conn.close()

def delete_case_by_id(case_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cases WHERE id = ?", (case_id,))
    conn.commit()
    conn.close()

def validate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None
