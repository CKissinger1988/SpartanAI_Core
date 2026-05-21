import os
import re
import sys
import subprocess

# ANSI Colors
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
BOLD = '\033[1m'
ENDC = '\033[0m'

# Files to delete entirely if they are dedicated to simulation/sandboxing
TRASH_FILES = [
    "scripts/purge_simulations.sh",
    "scripts/remove_simulations.py",
    "scripts/field_prep_secure.sh",
    "backend/core/sovereignty_upgrades.py", # Contains RedTeamSimulator
]

# Patterns to surgically remove from code
SURGICAL_PATTERNS = [
    # Command handlers in jeeves.py
    r'if command == "simulate breach":.*?return True\n',
    r'if command == "purge simulations":.*?return True\n',
    r'if command == "field prep":.*?return True\n',
    r'if command == "full production":.*?return True\n',
    # Imports related to simulation
    r'from backend\.core\.sovereignty_upgrades import .*?, RedTeamSimulator\n',
    # Comments related to simulation
    r'# Simulate.*?\n',
    r'# Mocking.*?\n',
]

def absolute_purge():
    print(f"{RED}{BOLD}--- NEXUS // AI: ABSOLUTE SANITIZATION ENGINE ---{ENDC}")
    
    # 1. Delete dedicated simulation files
    for file_path in TRASH_FILES:
        if os.path.exists(file_path):
            print(f"{CYAN}[-] Deleting dedicated simulation file: {file_path}{ENDC}")
            os.remove(file_path)
    
    # 2. Surgical removal from mixed-use files
    TARGET_FILES = [
        "backend/core/jeeves.py",
        "backend/core/sentinel.py",
        "backend/core/sovereignty.py",
        "scripts/nexus_ssh.py",
        "scripts/test_jarvis_evolution.py",
        "JarvisAI_Stable/main.py",
        "GEMINI.md"
    ]
    
    for file_path in TARGET_FILES:
        if not os.path.exists(file_path):
            continue
            
        print(f"{CYAN}[*] Sanitizing file: {file_path}{ENDC}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply surgical patterns
        for pattern in SURGICAL_PATTERNS:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Additional cleanup for specific logic blocks
        if file_path == "backend/core/jeeves.py":
            # Remove RedTeamSimulator import and usage more specifically if needed
            content = re.sub(r'from backend\.core\.sovereignty_upgrades import SwarmCoordinator, RedTeamSimulator', 'from backend.core.sovereignty_upgrades import SwarmCoordinator', content)

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"{GREEN}    -> Sanitization applied.{ENDC}")
        else:
            print(f"    -> No simulation traces found.")

    # 3. Update GEMINI.md with Zero Simulation Policy
    if os.path.exists("GEMINI.md"):
        policy = "\n- **Zero Simulation Policy:** All code, configuration, and tools must be designed for real-world, production-grade operations only. Simulation, sandboxing, and mock-logic are strictly prohibited to maintain operational integrity.\n"
        with open("GEMINI.md", 'r', encoding='utf-8') as f:
            gemini_content = f.read()
        
        if "Zero Simulation Policy" not in gemini_content:
            # Insert before Directories section
            if "## Directories" in gemini_content:
                gemini_content = gemini_content.replace("## Directories", "## Policy" + policy + "\n## Directories")
            else:
                gemini_content += "\n## Policy" + policy
            
            with open("GEMINI.md", 'w', encoding='utf-8') as f:
                f.write(gemini_content)
            print(f"{GREEN}[+] Zero Simulation Policy codified in GEMINI.md.{ENDC}")

    # 4. Cleanup Kali WSL
    print(f"{CYAN}[*] Synchronizing sanitization to WSL Kali...{ENDC}")
    wsl_cmds = [
        "rm -rf ~/nexusai/scripts/purge_simulations.sh",
        "rm -rf ~/nexusai/scripts/remove_simulations.py",
        "rm -rf ~/nexusai/scripts/field_prep_secure.sh",
        "rm -rf ~/nexusai/backend/core/sovereignty_upgrades.py",
        "find ~/nexusai -name '*mock_system*' -type d -exec rm -rf {} +",
    ]
    for cmd in wsl_cmds:
        subprocess.run(["wsl", "-d", "kali-linux", "bash", "-c", cmd])
    
    print(f"{RED}{BOLD}--- ABSOLUTE SANITIZATION COMPLETE ---{ENDC}")

if __name__ == "__main__":
    absolute_purge()
