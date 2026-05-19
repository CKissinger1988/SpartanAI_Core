import subprocess
import os
import sys

def initialize_environment():
    print("Sentinel Hub: Initializing Environment...")
    
    # 1. Ensure Kali/WSL is reachable
    try:
        subprocess.run(["wsl", "-d", "kali-linux", "whoami"], capture_output=True, check=True)
        print("WSL Kali instance detected.")
    except subprocess.CalledProcessError:
        print("Error: WSL Kali instance not found. Please install Kali Linux via WSL.")
        return False
    
    # 2. Setup Persistence/Updates
    print("Syncing persistent storage and checking updates...")
    subprocess.run(["wsl", "-d", "kali-linux", "sudo", "apt-get", "update"], capture_output=True)
    
    print("Environment initialized.")
    return True

if __name__ == "__main__":
    if initialize_environment():
        sys.exit(0)
    else:
        sys.exit(1)
