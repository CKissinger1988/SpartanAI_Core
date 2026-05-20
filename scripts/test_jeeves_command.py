import sys
import os

# Add root to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.jeeves import Jeeves

def test_command(cmd):
    jeeves = Jeeves()
    print(f"\nCommand: '{cmd}'")
    if not jeeves.handle_command(cmd):
        print("Jeeves: Command not recognized.")

if __name__ == "__main__":
    test_command("systems check")
    test_command("systems status")
    test_command("hello")
