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
                production_count INTEGER NOT NULL,
                source TEXT NOT NULL DEFAULT 'SIMULATOR'
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS alarms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                alarm TEXT NOT NULL,
                severity TEXT NOT NULL,
                acknowledged INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS production_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                status TEXT NOT NULL,
                production_count INTEGER NOT NULL
            )
            """
        )
        connection.commit()


def ensure_schema():
    """Add columns needed by newer versions without breaking old databases."""
    with get_connection() as connection:
        columns = {row[1] for row in connection.execute("PRAGMA table_info(readings)")}
        if "source" not in columns:
            connection.execute("ALTER TABLE readings ADD COLUMN source TEXT NOT NULL DEFAULT 'SIMULATOR'")
        connection.commit()
