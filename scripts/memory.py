import sqlite3
import pathlib

# Path to memory database
ROOT = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "memory.db"

def init_memory():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            importance INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def save_memory(text, importance=1):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO memories (text, importance) VALUES (?, ?)", (text, importance))
    conn.commit()
    conn.close()

def search_memory(query, limit=3):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT text FROM memories 
        WHERE text LIKE ? 
        ORDER BY importance DESC, id DESC 
        LIMIT ?
    """, (f"%{query}%", limit))
    results = [row[0] for row in c.fetchall()]
    conn.close()
    return results

def get_all_memories():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, text FROM memories ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_memory_by_query(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM memories WHERE text LIKE ?", (f"%{query}%",))
    conn.commit()
    conn.close()

def delete_all_memories():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM memories")
    conn.commit()
    conn.close()
