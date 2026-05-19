import subprocess
import os
import sys

def initialize_linux_environment():
    print("NexusAI: Initializing Bare Metal Kali Environment...")
    
    # 1. Check for Sudo/Root Privileges
    if os.geteuid() != 0:
        print("Warning: NexusAI is not running as root. Some security tools may be restricted.")
    
    # 2. Check for Essential Security Tools
    tools = ["nmap", "msfconsole", "sqlmap", "airmon-ng"]
    for tool in tools:
        if subprocess.run(["which", tool], capture_output=True).returncode == 0:
            print(f"  -> {tool}: Installed")
        else:
            print(f"  -> {tool}: NOT FOUND")
    
    # 3. Network Interface Check
    print("Checking network interfaces...")
    subprocess.run(["ip", "addr"], capture_output=True)
    
    print("Environment initialization complete.")
    return True

if __name__ == "__main__":
    if initialize_linux_environment():
        sys.exit(0)
    else:
        sys.exit(1)
