import sys
import os

# Add root to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.jeeves import Jeeves

def run_command(jeeves, cmd):
    print(f"\nCommand: '{cmd}'")
    if not jeeves.handle_command(cmd):
        print("Jeeves: Command not recognized.")

if __name__ == "__main__":
    jeeves = Jeeves()
    run_command(jeeves, "systems check") # Should fail
    run_command(jeeves, "login")         # Should succeed
    run_command(jeeves, "systems check") # Should succeed
