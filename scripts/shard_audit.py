import os
import sys

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ANSI Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
ENDC = '\033[0m'

def audit_shards():
    core_dir = "backend/core"
    services_dir = "backend/core/services"
    
    print(f"\n{CYAN}{BOLD}--- SpartanAI // Shard Tactical Audit ---{ENDC}")
    
    def scan_dir(directory, label):
        print(f"\n{BOLD}[{label}]{ENDC}")
        files = [f for f in os.listdir(directory) if f.endswith('.py') and not f.startswith('__')]
        
        for file in sorted(files):
            path = os.path.join(directory, file)
            size = os.path.getsize(path)
            
            status = f"{GREEN}Functional{ENDC}"
            if size < 100:
                status = f"{RED}Stub{ENDC}"
            elif size < 500:
                status = f"{YELLOW}Minimal / Incomplete{ENDC}"
            
            print(f"  {file:<40} : {status} ({size} bytes)")

    if os.path.exists(core_dir):
        scan_dir(core_dir, "Core Shards")
    
    if os.path.exists(services_dir):
        scan_dir(services_dir, "Service Shards")

if __name__ == "__main__":
    audit_shards()
