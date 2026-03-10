# database/db_connection.py
import sqlite3

def get_connection():
    conn = sqlite3.connect("moments_planner.db")
    conn.row_factory = sqlite3.Row
    return conn