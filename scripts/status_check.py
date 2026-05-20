import os
import sqlite3
import json
import sys
import random

# ANSI Colors for Dark Pentester Theme
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
BOLD = '\033[1m'
ENDC = '\033[0m'

# Add root to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_bar(percentage, length=20):
    """Creates a text-based progress bar with color."""
    filled = int(length * (percentage / 100))
    bar = '█' * filled + '-' * (length - filled)
    color = GREEN if percentage < 75 else RED
    return f"{color}|{bar}| {percentage:>3}%{ENDC}"

def check_jarvis_status():
    """Reports status and performance metrics with dark pentester styling."""
    status_report = {
        "NexusIntelligenceDB": "Offline",
        "JeevesOrchestrator": "Offline",
        "C2Uplink": "Offline",
        "Systems": "Nominal"
    }

    # Simulate Metrics
    metrics = {
        "Read/Write Speed": random.randint(10, 95),
        "System Load": random.randint(5, 80),
        "Memory Usage": random.randint(20, 90),
        "Database Size": random.randint(30, 99)
    }

    # Check Database
    if os.path.exists("nexus_intelligence.db"):
        try:
            conn = sqlite3.connect("nexus_intelligence.db")
            conn.close()
            status_report["NexusIntelligenceDB"] = "Online"
        except:
            status_report["NexusIntelligenceDB"] = "Error"

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

    print(f"\n{CYAN}{BOLD}--- NEXUS // AI // TACTICAL STATUS ---{ENDC}")
    for system, status in status_report.items():
        color = GREEN if status in ["Online", "Active", "Nominal"] else RED
        print(f"{BOLD}{system:<25}{ENDC}: {color}{status}{ENDC}")

    print(f"\n{CYAN}{BOLD}--- NEXUS // PERFORMANCE METRICS ---{ENDC}")
    for metric, value in metrics.items():
        print(f"{BOLD}{metric:<25}{ENDC}: {create_bar(value)}")

if __name__ == "__main__":
    check_jarvis_status()
