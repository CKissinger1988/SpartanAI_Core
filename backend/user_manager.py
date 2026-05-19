import sqlite3
import os
import hashlib
import binascii
import json
import sys
import logging

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UserManager")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            salt TEXT,
            role TEXT,
            last_login TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
    # Create default users if none exist
    create_default_users()

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt.decode('ascii'), pwdhash.decode('ascii'))

def verify_password(stored_password, provided_password, salt):
    """Verify a stored password against one provided by user."""
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), 
                                salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def add_user(username, password, role='operator'):
    salt, pwdhash = hash_password(password)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password_hash, salt, role)
            VALUES (?, ?, ?, ?)
        ''', (username, pwdhash, salt, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def create_default_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        logger.info("Creating default users...")
        add_user('ADMIN_CORE', 'NEXUS_ADMIN_2026', 'admin')
        add_user('OPERATOR_01', 'SENTINEL_PASS', 'operator')
    conn.close()

def authenticate(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash, salt, role FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        stored_hash, salt, role = row
        if verify_password(stored_hash, password, salt):
            return {"status": "success", "username": username, "role": role}
    
    return {"status": "error", "message": "INVALID CREDENTIALS"}

if __name__ == "__main__":
    init_db()
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "auth" and len(sys.argv) > 3:
            print(json.dumps(authenticate(sys.argv[2], sys.argv[3])))
        elif command == "add" and len(sys.argv) > 4:
            print(json.dumps({"success": add_user(sys.argv[2], sys.argv[3], sys.argv[4])}))
    else:
        print(json.dumps({"status": "ready"}))
