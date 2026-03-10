# services/auth_service.py
import hashlib
from database.db_connection import get_connection
import sqlite3  

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(full_name, phone_number, username, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (full_name, phone_number, username, email, password, role) VALUES (?, ?, ?, ?, ?, 'client')",
            (full_name, phone_number, username, email, hash_password(password))
        )
        conn.commit()
        print(f"Account for {full_name} created successfully!")
        return True
    except Exception as e:
        print("Signup error:", e)
        return False
    finally:
        conn.close()

def login(identifier, password):
    conn = get_connection()
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? OR email=?", (identifier, identifier))
    row = cursor.fetchone()
    conn.close()
    if row and row["password"] == hash_password(password):
        return {
            "id": row["id"],
            "full_name": row["full_name"],
            "phone_number": row["phone_number"],
            "username": row["username"],
            "email": row["email"],
            "role": row["role"]
        }
    return None