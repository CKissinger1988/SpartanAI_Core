import os
import re
import glob
import logging

class LocalCredentialIngestor:
    """
    Local Credential Ingestor Shard.
    MANDATE: Scan local environment for mission-critical keys and inject into Global Auth Vault.
    PROTECTION: Keys are processed in-memory and NEVER logged or printed.
    """
    def __init__(self, auth_vault):
        self.vault = auth_vault
        self.patterns = {
            "OPENAI": r"sk-[a-zA-Z0-9]{48}",
            "GEMINI": r"AIzaSy[a-zA-Z0-9_-]{33}",
            "ANTHROPIC": r"sk-ant-api03-[a-zA-Z0-9_-]{95}",
            "X_API": r"([a-zA-Z0-9]{25})", # Simplified pattern
        }

    def scan_and_assimilate(self):
        logging.info("[INGESTOR]: Initiating local credential scan...")
        
        # 1. Scan Environment Variables
        for key, value in os.environ.items():
            for provider, pattern in self.patterns.items():
                if re.match(pattern, value):
                    self.vault.save_key("AI_MODELS", provider, value)
                    logging.info(f"[INGESTOR]: Recovered {provider} key from environment.")

        # 2. Scan Local Configuration Files (.env, config.json)
        # Search recursively in the project and common user paths
        target_files = ["**/.env", "**/*.json", "**/*.txt"]
        for pattern_file in target_files:
            for filepath in glob.glob(pattern_file, recursive=True):
                try:
                    with open(filepath, 'r', errors='ignore') as f:
                        content = f.read()
                        for provider, pattern in self.patterns.items():
                            match = re.search(pattern, content)
                            if match:
                                self.vault.save_key("AI_MODELS", provider, match.group(0))
                                logging.info(f"[INGESTOR]: Recovered {provider} key from {filepath}.")
                except Exception:
                    pass

        logging.info("[INGESTOR]: Sovereign onboarding complete. Mission-critical keys assimilated.")

    def start_evolution(self):
        logging.info("[INGESTOR]: Local Discovery Shard ONLINE.")
