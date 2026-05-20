import os
import sqlite3
import json
import sys

# Add root to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_jarvis_status():
    """Reports status of core JarvisAI components and databases."""
    status_report = {
        "NexusIntelligenceDB": "Offline",
        "JeevesOrchestrator": "Offline",
        "C2Uplink": "Offline",
        "Systems": "Nominal"
    }

    # Check Database
    if os.path.exists("nexus_intelligence.db"):
        try:
            conn = sqlite3.connect("nexus_intelligence.db")
            conn.close()
            status_report["NexusIntelligenceDB"] = "Online"
        except:
            status_report["NexusIntelligenceDB"] = "Error"

    # Check Jeeves (Mocking import for demo purposes)
    try:
        from backend.core.jeeves import Jeeves
        jeeves = Jeeves()
        status_report["JeevesOrchestrator"] = jeeves.get_status()
    except:
        status_report["JeevesOrchestrator"] = "Error"

    # Check C2 Uplink (mock check)
    if os.path.exists("gate.key"):
        status_report["C2Uplink"] = "Active"

    print("--- JarvisAI Tactical Status ---")
    for system, status in status_report.items():
        print(f"{system:<25}: {status}")

if __name__ == "__main__":
    check_jarvis_status()
