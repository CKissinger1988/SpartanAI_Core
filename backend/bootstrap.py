import sqlite3
import os
import sys
import subprocess
import logging

# Path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'exploits.db')
JARVIS_DIR = os.path.join(BASE_DIR, '..', 'JarvisAI_Stable')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Bootstrap")

def init_db():
    logger.info("Initializing Exploit Database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exploits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cve_id TEXT,
            name TEXT,
            type TEXT,
            source_url TEXT UNIQUE,
            content TEXT,
            date_added TEXT
        )
    ''')
    
    # Check if empty
    cursor.execute('SELECT COUNT(*) FROM exploits')
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        logger.info("Database empty. Importing initial 2025/2026 signatures...")
        try:
            from exploit_manager import auto_update_msf
            auto_update_msf()
        except ImportError:
            logger.error("Could not import exploit_manager to populate database.")

def setup_jarvis():
    logger.info("Configuring Jarvis AI environment...")
    # Ensure secret.key exists so Jarvis doesn't crash
    key_file = os.path.join(JARVIS_DIR, 'secret.key')
    if not os.path.exists(key_file):
        try:
            from config_manager import generate_key
            # We need to be in the Jarvis dir or add it to path
            sys.path.append(JARVIS_DIR)
            import config_manager
            config_manager.KEY_FILE = key_file # ensure it uses the right path
            config_manager.generate_key()
            logger.info("Jarvis security key generated.")
        except Exception as e:
            logger.error(f"Failed to generate Jarvis key: {e}")

def check_os_environment():
    logger.info(f"Checking OS environment: {sys.platform}")
    if sys.platform == "win32":
        try:
            subprocess.run(["wsl", "-d", "kali-linux", "whoami"], capture_output=True, check=True)
            logger.info("WSL Kali instance detected.")
        except:
            logger.warning("WSL Kali instance not found. Some 'MAIN_SHELL' tools may be unavailable.")
    else:
        # Check for core tools on Linux
        tools = ["nmap", "msfconsole", "sqlmap"]
        for tool in tools:
            if subprocess.run(["which", tool], capture_output=True).returncode == 0:
                logger.info(f"System tool found: {tool}")
            else:
                logger.warning(f"System tool NOT found: {tool}")

def bootstrap():
    logger.info("--- NEXUS // AI BOOTSTRAP STARTING ---")
    init_db()
    setup_jarvis()
    check_os_environment()
    logger.info("--- BOOTSTRAP COMPLETE. READY FOR UPLINK. ---")

if __name__ == "__main__":
    bootstrap()
