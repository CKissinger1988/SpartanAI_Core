import subprocess
import os

# ANSI Colors for Dark Pentester Theme
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
BOLD = '\033[1m'
ENDC = '\033[0m'

def Jarvis_login():
    """Simulates an SSH-based login portal for The Creator."""
    print(f"\n{CYAN}{BOLD}Jarvis // AI // CREATOR ACCESS PORTAL{ENDC}")
    print(f"{CYAN}Establishing encrypted uplink...{ENDC}")
    username = input(f"{BOLD}User: {ENDC}")
    if username != "Creator":
        print(f"{RED}Access Denied: Unrecognized User.{ENDC}")
        return

    password = input(f"{BOLD}Passphrase: {ENDC}")
    # In a real scenario, this would check against a secure vault
    if password in ["@11646", "C:\\GitHub\\.ssh\\SpartanAI-Core.pem"]:
        print(f"\n{GREEN}{BOLD}Authentication Successful. Welcome, Creator.{ENDC}")
        print(f"{CYAN}Session encrypted. Launching Jeeves Terminal...{ENDC}")
        
        # Trigger the main Jeeves interface loop
        from backend.core.jeeves import Jeeves
        jeeves = Jeeves()
        jeeves.handle_command("login")
        
        while True:
            cmd = input(f"\n{BOLD}Jarvis > {ENDC}")
            if cmd.lower() in ["exit", "logout"]:
                print(f"{CYAN}Terminating session...{ENDC}")
                break
            jeeves.handle_command(cmd)
    else:
        print(f"{RED}Authentication Failed.{ENDC}")

if __name__ == "__main__":
    Jarvis_login()
