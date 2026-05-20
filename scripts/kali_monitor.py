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

def apply_updates():
    """Automatically applies all available apt updates."""
    try:
        print(f"[*] Jarvis: Initiating Autonomous System Patching at {datetime.now()}")
        subprocess.run(["apt-get", "dist-upgrade", "-y"], check=True)
        subprocess.run(["apt-get", "autoremove", "-y"], check=True)
        subprocess.run(["apt-get", "clean"], check=True)
        print("[+] Jarvis: System Patching Complete.")
        return True
    except Exception as e:
        print(f"[!] Jarvis Update Error: {str(e)}")
        return False

def monitor_updates():
    """Main loop for monitoring and applying updates."""
    print(f"[*] Jarvis Kali Monitor Started at {datetime.now()}")
    AUTO_UPDATE = os.environ.get("JARVIS_AUTO_PATCH", "true") == "true"
    
    if not os.path.exists(os.path.dirname(STATE_FILE)):
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

    while True:
        updates = get_apt_updates()
        current_version = get_kali_version()
        
        status = {
            "timestamp": datetime.now().isoformat(),
            "kali_version": current_version,
            "update_count": len(updates),
            "packages": updates[:10],
            "auto_patch_enabled": AUTO_UPDATE
        }

        # Write to state file for Jarvis to read
        with open(STATE_FILE, "w") as f:
            json.dump(status, f, indent=4)
        
        if updates:
            print(f"[!] {len(updates)} updates available.")
            if AUTO_UPDATE:
                apply_updates()
                # Re-check after update
                updates = []
        else:
            print("[*] System is up to date.")

        # Check every 6 hours
        time.sleep(21600)

if __name__ == "__main__":
    monitor_updates()
