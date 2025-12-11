# backend/memory/memory_core.py

import sqlite3
from pathlib import Path


class MemoryManager:
    """
    SQLite-based memory system.
    Handles storing, searching, listing, and deleting memories.
    """

    def __init__(self, config=None):
        # Locate database in project root (not in backend/)
        project_root = Path(__file__).resolve().parents[2]
        self.db_path = project_root / "memory.db"

        # Ensure DB exists
        self._init_db()

    # ------------------------------------------------------
    # Internal: initialize database
    # ------------------------------------------------------
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
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

    # ------------------------------------------------------
    # Save memory
    # ------------------------------------------------------
    def store(self, user_id: str, text: str, importance: int = 1):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO memories (text, importance) VALUES (?, ?)",
            (text, importance)
        )
        conn.commit()
        conn.close()

    # ------------------------------------------------------
    # Keyword search
    # ------------------------------------------------------
    def query(self, user_id: str, query_text: str, top_k: int = 3):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            SELECT text FROM memories
            WHERE text LIKE ?
            ORDER BY importance DESC, id DESC
            LIMIT ?
        """, (f"%{query_text}%", top_k))
        results = [row[0] for row in c.fetchall()]
        conn.close()
        return results

    # ------------------------------------------------------
    # List all memories
    # ------------------------------------------------------
    def list_all(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id, text FROM memories ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        return rows

    # ------------------------------------------------------
    # Delete by query
    # ------------------------------------------------------
    def delete_by_query(self, query_text: str):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM memories WHERE text LIKE ?", (f"%{query_text}%",))
        conn.commit()
        conn.close()

    # ------------------------------------------------------
    # Delete all memories
    # ------------------------------------------------------
    def delete_all(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM memories")
        conn.commit()
        conn.close()
