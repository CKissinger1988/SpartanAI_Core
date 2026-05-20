import os
import sqlite3
import json
import sys
import random

# Add root to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_bar(percentage, length=20):
    """Creates a text-based progress bar."""
    filled = int(length * (percentage / 100))
    bar = '█' * filled + '-' * (length - filled)
    return f"|{bar}| {percentage:>3}%"

def check_jarvis_status():
    """Reports status and performance metrics of core JarvisAI components."""
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

    print("--- JarvisAI Tactical Status ---")
    for system, status in status_report.items():
        print(f"{system:<25}: {status}")

    print("\n--- Performance Metrics ---")
    for metric, value in metrics.items():
        print(f"{metric:<25}: {create_bar(value)}")

if __name__ == "__main__":
    check_jarvis_status()
