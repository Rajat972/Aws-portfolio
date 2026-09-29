import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "portfolio.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the SQLite database schema if not already present."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notified_via_email INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def save_contact_message(name: str, email: str, subject: str, message: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Dict[str, Any]:
    """Save a new contact submission into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO contact_messages (name, email, subject, message, ip_address, user_agent, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, email, subject, message, ip_address, user_agent, now_str))
    
    msg_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": msg_id,
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "created_at": now_str
    }

def update_email_notified_status(msg_id: int, status: bool = True):
    """Mark a message as successfully emailed."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE contact_messages SET notified_via_email = ? WHERE id = ?", (1 if status else 0, msg_id))
    conn.commit()
    conn.close()

def get_all_contact_messages(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve submitted messages from database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
