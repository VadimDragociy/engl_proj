import sqlite3
from .config import DB_PATH
import datetime as dt

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            created_at TEXT
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS samples (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            image_path TEXT,
            embedding BLOB,
            created_at TEXT
        )
        """)

def add_sample(name, image_path, embedding):
    with get_conn() as conn:
        cur = conn.execute("SELECT id FROM people WHERE name=?", (name,))
        row = cur.fetchone()

        if row:
            person_id = row[0]
        else:
            cur = conn.execute(
                "INSERT INTO people(name, created_at) VALUES(?, ?)",
                (name, dt.datetime.utcnow().isoformat())
            )
            person_id = cur.lastrowid

        conn.execute("""
        INSERT INTO samples(person_id, image_path, embedding, created_at)
        VALUES (?, ?, ?, ?)
        """, (person_id, image_path, embedding.tobytes(), dt.datetime.utcnow().isoformat()))

def load_all_embeddings():
    names = []
    embeddings = []

    with get_conn() as conn:
        rows = conn.execute("""
        SELECT p.name, s.embedding
        FROM samples s
        JOIN people p ON p.id = s.person_id
        """).fetchall()

    import numpy as np
    for name, blob in rows:
        emb = np.frombuffer(blob, dtype=np.float32)
        names.append(name)
        embeddings.append(emb)

    return names, embeddings
