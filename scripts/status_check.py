import os
import sqlite3
import sys
import json
from dotenv import load_dotenv

# Load Sovereign Environment
load_dotenv()

# ANSI Colors for Dark Pentester Theme
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
ENDC = '\033[0m'

# Add root to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_jarvis_status():
    """Reports status with dark pentester styling."""
    status_report = {
        "JarvisIntelligenceDB": "Offline",
        "JeevesOrchestrator": "Offline",
        "C2Uplink": "Offline",
        "LND_Node": "Offline",
        "StealthMiner": "Inactive",
        "Systems": "Nominal"
    }

    # Check Database
    if os.path.exists("vector_db/chroma.sqlite3"):
        try:
            conn = sqlite3.connect("vector_db/chroma.sqlite3")
            conn.close()
            status_report["JarvisIntelligenceDB"] = "Online"
        except:
            status_report["JarvisIntelligenceDB"] = "Error"

    # Check Jeeves
    try:
        from backend.core.jeeves import Jeeves
        jeeves = Jeeves()
        status_report["JeevesOrchestrator"] = "Online" # If it initializes
    except:
        status_report["JeevesOrchestrator"] = "Error"

    # Check C2 Uplink
    if os.path.exists("gate.key"):
        status_report["C2Uplink"] = "Active"

    # Check LND
    try:
        from backend.core.lnd_manager import LNDManager
        lnd = LNDManager()
        if os.path.exists(lnd.macaroon_path):
            status_report["LND_Node"] = "Ready (Credentials Found)"
        else:
            status_report["LND_Node"] = "Missing Credentials"
    except:
        status_report["LND_Node"] = "Error"

    # Check Stealth Miner
    import psutil
    miner_active = False
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            if 'xmrig' in proc.info['name'].lower() or \
               (proc.info['exe'] and 'SpartanAI_Core\\tools\\miner' in proc.info['exe']):
                miner_active = True
                break
        except: pass
    
    if miner_active:
        status_report["StealthMiner"] = "Online (Active)"

    print(f"\n{CYAN}{BOLD}--- Jarvis // AI // TACTICAL STATUS ---{ENDC}")
    for system, status in status_report.items():
        color = GREEN if "Online" in status or "Active" in status or "Ready" in status or status == "Nominal" else \
                YELLOW if "Credentials" in status else RED
        print(f"{BOLD}{system:<25}{ENDC}: {color}{status}{ENDC}")

if __name__ == "__main__":
    check_jarvis_status()
