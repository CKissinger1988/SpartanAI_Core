import sys
import os

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.jarvis import Jarvis

def run_test():
    jarvis = Jarvis()
    
    print("\n--- TEST 1: Public Scan Threats ---")
    jarvis.handle_command("scan threats")
    
    print("\n--- TEST 2: High Risk Command (Public) ---")
    jarvis.handle_command("sudo rm -rf /") # Should be blocked but logged
    
    print("\n--- TEST 3: Login and View Observations ---")
    jarvis.handle_command("login")
    jarvis.handle_command("view observations")
    
    print("\n--- TEST 4: Systems Status ---")
    jarvis.handle_command("systems status")

if __name__ == "__main__":
    run_test()
