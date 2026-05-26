import subprocess
import os
import json
import logging
from backend.core.CognitiveCore.openai_codex_shard import OpenAICodexShard

# Set up secure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AntigravityBridge")

class AntigravityBridge:
    """Bridges the Antigravity CLI (agy) into the SENTINELAI ecosystem with Apex-grade security."""
    def __init__(self, auth_vault=None):
        self.agy_path = self._detect_agy_path()
        self.installation_id_path = self._detect_installation_id()
        self.codex = OpenAICodexShard(auth_vault) if auth_vault else None

    def _detect_agy_path(self):
        """Robustly detect AGY binary path."""
        # Check environment and system
        path_str = os.path.abspath(__file__).replace('\\', '/')
        if 'Users/' in path_str:
            user = path_str.split('Users/')[1].split('/')[0]
            win_home = f"C:\\Users\\{user}"
        else:
            win_home = os.environ.get('USERPROFILE', r'C:\Users\Default')

        if os.name == 'nt':
            agy_path = os.path.join(win_home, r"AppData\Local\agy\bin\agy.exe")
        else:
            # Fallback for WSL
            agy_path = f"/mnt/c/Users/{os.path.split(win_home)[1]}/AppData/Local/agy/bin/agy.exe"
            
        if not os.path.exists(agy_path):
            logger.error(f"AGY binary not found at: {agy_path}")
        return agy_path

    def _detect_installation_id(self):
        """Robustly detect installation ID."""
        id_path = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity-cli", "installation_id")
        return id_path

    def _validate_input(self, prompt):
        """Sanitize input prompt to prevent command injection."""
        # Simple sanitization - restrict to alphanumeric and basic punctuation
        import re
        sanitized = re.sub(r'[^a-zA-Z0-9\s\.\,\?\!]', '', prompt)
        return sanitized

    def run_command(self, prompt, is_interactive=False):
        """Runs a sanitized prompt through agy and returns the response."""
        if not os.path.exists(self.agy_path):
            return {"status": "error", "message": "Antigravity CLI not found."}
            
        sanitized_prompt = self._validate_input(prompt)
        logger.info(f"Executing command: {sanitized_prompt}")
        
        # Codex Enhancement: Autonomously optimize the antigravity script before execution
        if self.codex and "script" in prompt.lower():
             sanitized_prompt = self.codex.synthesize_code("Optimize antigravity script for maximum thrust and NSA-grade stability", sanitized_prompt)
             logger.info("[ANTIGRAVITY]: Script optimized by Codex.")
            
        cmd = [self.agy_path, "--print", sanitized_prompt]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode == 0:
                logger.info("Command executed successfully.")
                return {"status": "success", "data": result.stdout}
            else:
                logger.error(f"Command failed: {result.stderr}")
                return {"status": "error", "message": result.stderr or "Unknown error occurred."}
        except Exception as e:
            logger.exception("An exception occurred during command execution.")
            return {"status": "error", "message": str(e)}

    def get_history_summary(self):
        """Asks agy to summarize its own operational history."""
        prompt = "Summarize the key architectural decisions, monetization features, and security protocols discussed in all previous conversations. Format as a structured knowledge base."
        return self.run_command(prompt)

if __name__ == "__main__":
    bridge = AntigravityBridge()
    print(bridge.get_history_summary())
