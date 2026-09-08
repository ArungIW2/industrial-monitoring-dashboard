import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("monitoring.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL NOT NULL,
                rpm INTEGER NOT NULL,
                voltage REAL NOT NULL,
                current REAL NOT NULL,
                machine_status TEXT NOT NULL,
                alarm TEXT NOT NULL,
                production_count INTEGER NOT NULL
            )
            """
        )
        connection.commit()
