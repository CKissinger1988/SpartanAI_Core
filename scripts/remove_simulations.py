import subprocess
import sys
import os

# ANSI Colors for Dark Pentester Theme
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
BOLD = '\033[1m'
ENDC = '\033[0m'

def run_purge(mode="standard"):
    if mode == "full-prod":
        print(f"{RED}{BOLD}NEXUS // AI // FULL PRODUCTION ARSENAL ENABLEMENT{ENDC}")
    elif mode == "field":
        print(f"{RED}{BOLD}NEXUS // AI // SECURE FIELD SANITIZATION ORCHESTRATOR{ENDC}")
    else:
        print(f"{CYAN}{BOLD}NEXUS // AI // SIMULATION PURGE ORCHESTRATOR{ENDC}")
    
    # Identify environment
    if sys.platform == "win32":
        print(f"{CYAN}Detected Windows host. Targeting WSL Kali instance...{ENDC}")
        try:
            # Check if nexusai exists in Kali
            target_dir = "~/nexusai"
            check_cmd = f"if [ -d {target_dir} ]; then echo 'FOUND'; fi"
            result = subprocess.run(["wsl", "-d", "kali-linux", "bash", "-c", check_cmd], capture_output=True, text=True)
            
            if "FOUND" not in result.stdout:
                target_dir = "~/nexusai-security-suite"
                check_cmd = f"if [ -d {target_dir} ]; then echo 'FOUND'; fi"
                result = subprocess.run(["wsl", "-d", "kali-linux", "bash", "-c", check_cmd], capture_output=True, text=True)
                if "FOUND" not in result.stdout:
                    print(f"{RED}Error: NexusAI installation not found in WSL Kali.{ENDC}")
                    return

            print(f"{CYAN}Targeting directory: {target_dir}{ENDC}")
            
            if mode == "full-prod":
                # Execute full production arsenal enablement
                purge_cmd = f"cd {target_dir} && bash scripts/production_enable.sh"
            elif mode == "field":
                # Execute aggressive field prep
                purge_cmd = f"""
                cd {target_dir}
                echo '[!] INITIATING SECURE FIELD PREP...'
                if [ -f scripts/field_prep_secure.sh ]; then
                    bash scripts/field_prep_secure.sh
                else
                    rm -f data/*.jsonl data/*.log 2>/dev/null
                    find . -name 'mock_system' -type d -exec rm -rf {{}} + 2>/dev/null
                    rm -rf workspace/ *.iso *.zip 2>/dev/null
                    rm -rf vector_db/* 2>/dev/null
                    rm -f INITIAL_CREDENTIALS.txt 2>/dev/null
                fi
                """
            else:
                # Standard purge
                purge_cmd = f"""
                cd {target_dir}
                echo '[+] Purging behavioral logs...'
                rm -f data/behavioral_observations.jsonl 2>/dev/null
                echo '[+] Purging mock systems...'
                find . -name 'mock_system' -type d -exec rm -rf {{}} + 2>/dev/null
                echo '[+] Purging build workspaces...'
                rm -rf workspace 2>/dev/null
                echo '[+] Clearing Python caches...'
                find . -type d -name '__pycache__' -not -path '*/venv/*' -not -path '*/node_modules/*' -exec rm -rf {{}} + 2>/dev/null
                """
            
            subprocess.run(["wsl", "-d", "kali-linux", "bash", "-c", purge_cmd])
            print(f"{GREEN}{BOLD}WSL Kali Operation Complete.{ENDC}")
            
        except Exception as e:
            print(f"{RED}Error executing WSL operation: {e}{ENDC}")
    else:
        # Native Linux execution
        if mode == "full-prod":
            script = "scripts/production_enable.sh"
        elif mode == "field":
            script = "scripts/field_prep_secure.sh"
        else:
            script = "scripts/purge_simulations.sh"
            
        print(f"{CYAN}Detected Linux host. Executing {script}...{ENDC}")
        try:
            subprocess.run(["bash", script], check=True)
        except Exception as e:
            print(f"{RED}Error executing native operation: {e}{ENDC}")

if __name__ == "__main__":
    if "--full-prod" in sys.argv:
        mode = "full-prod"
    elif "--field" in sys.argv or "--real-world" in sys.argv:
        mode = "field"
    else:
        mode = "standard"
    run_purge(mode)
