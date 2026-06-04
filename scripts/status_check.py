import os
import sqlite3
import sys

# ANSI Colors for Dark Pentester Theme
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
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
        status_report["JeevesOrchestrator"] = jeeves.get_status()
    except:
        status_report["JeevesOrchestrator"] = "Error"

    # Check C2 Uplink
    if os.path.exists("gate.key"):
        status_report["C2Uplink"] = "Active"

    print(f"\n{CYAN}{BOLD}--- Jarvis // AI // TACTICAL STATUS ---{ENDC}")
    for system, status in status_report.items():
        color = GREEN if status in ["Online", "Active", "Nominal"] else RED
        print(f"{BOLD}{system:<25}{ENDC}: {color}{status}{ENDC}")

if __name__ == "__main__":
    check_jarvis_status()
