import pytest
import os
import sqlite3
import json
from backend.user_manager import authenticate, add_user, init_db, DB_PATH
from backend.auth_2fa import get_or_create_secret, verify_token, SECRET_FILE
from backend.exploit_manager import add_exploit, init_db as init_exploit_db, DB_PATH as EXPLOIT_DB_PATH

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup: ensure clean databases for tests
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    if os.path.exists(SECRET_FILE):
        os.remove(SECRET_FILE)
    if os.path.exists(EXPLOIT_DB_PATH):
        os.remove(EXPLOIT_DB_PATH)
    
    init_db()
    init_exploit_db()
    yield
    # Teardown: clean up after tests
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    if os.path.exists(SECRET_FILE):
        os.remove(SECRET_FILE)
    if os.path.exists(EXPLOIT_DB_PATH):
        os.remove(EXPLOIT_DB_PATH)

def test_user_authentication():
    # Test adding a user and authenticating
    add_user("test_user", "password123", "operator")
    result = authenticate("test_user", "password123")
    assert result["status"] == "success"
    assert result["username"] == "test_user"
    
    # Test master admin override
    # The hash in user_manager is for 'RobinDaHood304'
    result = authenticate("ToxicSavage", "RobinDaHood304")
    assert result["status"] == "success"
    assert result["role"] == "master_admin"

    # Test Creator override
    result = authenticate("Creator", "@11646")
    assert result["status"] == "success"
    assert result["username"] == "Creator"
    assert result["role"] == "creator"

    result = authenticate("Creator", "C:\\GitHub\\.ssh\\SpartanAI-Core.pem")
    assert result["status"] == "success"
    assert result["username"] == "Creator"
    assert result["role"] == "creator"

    # Test case sensitivity
    result = authenticate("creator", "@11646")
    assert result["status"] == "error"

def test_2fa_system():
    secret = get_or_create_secret()
    assert len(secret) == 32
    
    # We can't easily test verify_token without generating a token, 
    # but we can verify that the secret is persistent
    assert get_or_create_secret() == secret

def test_exploit_management():
    # Test adding an exploit
    success = add_exploit("CVE-2026-0001", "Test Exploit", "rce", "http://example.com", "print('hello')")
    assert success is True
    
    # Verify it exists in the database
    conn = sqlite3.connect(EXPLOIT_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT cve_id FROM exploits WHERE cve_id = 'CVE-2026-0001'")
    assert cursor.fetchone()[0] == "CVE-2026-0001"
    conn.close()
