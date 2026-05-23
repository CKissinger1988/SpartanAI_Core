import subprocess
import os
import json

class AntigravityBridge:
    """Bridges the Antigravity CLI (agy) into the SENTINELAI ecosystem."""
    def __init__(self):
        # Detect environment and dynamic user
        path_str = os.path.abspath(__file__).replace('\\', '/')
        if 'Users/' in path_str:
            user = path_str.split('Users/')[1].split('/')[0]
            win_home = f"C:\\Users\\{user}"
            wsl_home = f"/mnt/c/Users/{user}"
        else:
            win_home = os.environ.get('USERPROFILE', r'C:\Users\Default')
            wsl_home = "/mnt/c/Users/Default"

        if os.name == 'nt':
            self.agy_path = os.path.join(win_home, r"AppData\Local\agy\bin\agy.exe")
        else:
            self.agy_path = f"{wsl_home}/AppData/Local/agy/bin/agy.exe"

        self.installation_id_path = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity-cli", "installation_id")
        if not os.path.exists(self.installation_id_path) and os.name != 'nt':
             # Fallback for WSL mount
             self.installation_id_path = f"{wsl_home}/.gemini/antigravity-cli/installation_id"

    def run_command(self, prompt, is_interactive=False):
        """Runs a prompt through agy and returns the response."""
        if not os.path.exists(self.agy_path):
            return {"status": "error", "message": "Antigravity CLI not found at expected path."}
            
        cmd = [self.agy_path, "--print", prompt]
        try:
            # Use shell=True on Windows to handle path spaces if needed, but list is better
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode == 0:
                return {"status": "success", "data": result.stdout}
            else:
                return {"status": "error", "message": result.stderr or "Unknown error occurred."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_history_summary(self):
        """Asks agy to summarize its own operational history for BrainBridge ingestion."""
        prompt = "Summarize the key architectural decisions, monetization features, and security protocols discussed in all previous conversations. Format as a structured knowledge base."
        return self.run_command(prompt)

if __name__ == "__main__":
    bridge = AntigravityBridge()
    print(bridge.get_history_summary())
