"""Leaderboard Class"""
import sqlite3
from .record import Record

class Leaderboard():
    def __init__(self, db_path: str = "leaderboard.db"):
        """Initialize Leaderboard with SQLite Database"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize Database Table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        navigate = conn.cursor()
        navigate.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                score INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_record(self, record: Record):
        """Add Record to Database"""
        conn = sqlite3.connect(self.db_path)
        navigate = conn.cursor()
        navigate.execute('INSERT INTO records (username, score) VALUES (?, ?)', (record.username, record.score))
        conn.commit()
        conn.close()
    
    def get_top_records(self, limit: int = 10) -> list[Record]:
        """Get Top Records from Database"""
        conn = sqlite3.connect(self.db_path)
        navigate = conn.cursor()
        navigate.execute('''
            SELECT username, score
            FROM records
            ORDER BY score DESC
            LIMIT ?
        ''', (limit,))
        results = navigate.fetchall()
        conn.close()
        return [Record(username, score) for username, score in results]