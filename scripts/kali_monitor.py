#!/usr/bin/env python3
import subprocess
import json
import os
import time
from datetime import datetime

# Path to store the last known update state
STATE_FILE = "/opt/nexus-ai/data/update_state.json"

def get_apt_updates():
    """Checks for available package updates via apt."""
    try:
        # Update package lists first
        subprocess.run(["apt-get", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        # List upgradable packages
        result = subprocess.run(["apt", "list", "--upgradable"], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        # Filter out the "Listing..." header
        updates = [line for line in lines if '/' in line]
        return updates
    except Exception as e:
        return [f"Error checking apt updates: {str(e)}"]

def get_kali_version():
    """Checks the current Kali Rolling version."""
    try:
        if os.path.exists("/etc/kali_version"):
            with open("/etc/kali_version", "r") as f:
                return f.read().strip()
    except:
        pass
    return "Unknown"

def monitor_updates():
    """Main loop for monitoring updates."""
    print(f"[*] Jarvis Kali Monitor Started at {datetime.now()}")
    
    if not os.path.exists(os.path.dirname(STATE_FILE)):
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

    while True:
        updates = get_apt_updates()
        current_version = get_kali_version()
        
        status = {
            "timestamp": datetime.now().isoformat(),
            "kali_version": current_version,
            "update_count": len(updates),
            "packages": updates[:10]  # Store first 10 for summary
        }

        # Write to state file for Jarvis to read
        with open(STATE_FILE, "w") as f:
            json.dump(status, f, indent=4)
        
        if updates:
            print(f"[!] {len(updates)} updates available. State updated for Jarvis.")
        else:
            print("[*] System is up to date.")

        # Check every 6 hours
        time.sleep(21600)

if __name__ == "__main__":
    monitor_updates()
