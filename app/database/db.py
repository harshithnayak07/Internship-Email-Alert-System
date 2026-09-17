import sqlite3
from datetime import datetime, timezone


def _get_db_path():
    from app.config import STATE_DB_PATH
    return STATE_DB_PATH


def get_connection():
    conn = sqlite3.connect(_get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS processed_emails (
            message_id TEXT PRIMARY KEY,
            classification TEXT,
            notification_sent INTEGER DEFAULT 0,
            processed_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def is_processed(message_id):
    conn = get_connection()
    cursor = conn.execute(
        "SELECT 1 FROM processed_emails WHERE message_id = ?", (message_id,)
    )
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def mark_processed(message_id, classification, notification_sent=True):
    conn = get_connection()
    conn.execute(
        """INSERT OR REPLACE INTO processed_emails
           (message_id, classification, notification_sent, processed_at)
           VALUES (?, ?, ?, ?)""",
        (message_id, classification, int(notification_sent), datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()
