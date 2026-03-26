import sqlite3
from datetime import datetime

DB_PATH = "data/cases.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id TEXT PRIMARY KEY,
        sygnatura TEXT,
        created_at TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT,
        type TEXT,
        side TEXT,
        content TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_case(case_id, signature):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO cases (id, signature, created_at) VALUES (?, ,?)",
        (case_id, signature, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def add_document(case_id, doc_type, side, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO documents (case_id, type, side, content, created_at) VALUES (?, ?, ?, ?, ?)",
        (case_id, doc_type, side, content, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_case(case_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    case = c.fetchone()

    c.execute("SELECT * FROM documents WHERE case_id = ?", (case_id,))
    docs = c.fetchall()

    conn.close()

    return {
        "case": case,
        "documents": docs
    }