import os
import re
import glob
import logging
import sqlite3
import shutil
import tempfile

class DeepCredentialIngestor:
    """
    Deep Credential Ingestor Shard (v2.0).
    MANDATE: Scan local environment, environment variables, and browser history for credentials.
    PROTECTION: Keys are processed in-memory and NEVER logged or printed.
    """
    def __init__(self, auth_vault):
        self.vault = auth_vault
        self.patterns = {
            "OPENAI": r"sk-[a-zA-Z0-9]{48}",
            "GEMINI": r"AIzaSy[a-zA-Z0-9_-]{33}",
            "ANTHROPIC": r"sk-ant-api03-[a-zA-Z0-9_-]{95}",
            "X_API": r"([a-zA-Z0-9]{25})",
        }
        self.browser_paths = {
            "CHROME": os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\History"),
            "EDGE": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History"),
            "FIREFOX": os.path.expandvars(r"%APPDATA%\Mozilla\Firefox\Profiles\*.default-release\places.sqlite")
        }

    def scan_and_assimilate(self):
        logging.info("[DEEP-INGESTOR]: Initiating local credential scan...")
        
        # 1. Environment Variables
        self._scan_env()

        # 2. Local Files (.env, etc.)
        self._scan_files()

        # 3. Web History (NEW)
        self._scan_web_history()

        logging.info("[DEEP-INGESTOR]: Sovereign onboarding complete. All vectors analyzed.")

    def _scan_env(self):
        for key, value in os.environ.items():
            for provider, pattern in self.patterns.items():
                if re.match(pattern, value):
                    self.vault.save_key("AI_MODELS", provider, value)
                    logging.info(f"[DEEP-INGESTOR]: Recovered {provider} key from environment.")

    def _scan_files(self):
        target_files = ["**/.env", "**/*.json", "**/*.txt", "**/*.sh", "**/*.ps1"]
        for pattern_file in target_files:
            for filepath in glob.glob(pattern_file, recursive=True):
                try:
                    with open(filepath, 'r', errors='ignore') as f:
                        content = f.read()
                        for provider, pattern in self.patterns.items():
                            match = re.search(pattern, content)
                            if match:
                                self.vault.save_key("AI_MODELS", provider, match.group(0))
                                logging.info(f"[DEEP-INGESTOR]: Recovered {provider} key from {filepath}.")
                except Exception: pass

    def _scan_web_history(self):
        """Attempts to read browser history for credential leakage or login patterns."""
        for browser, path in self.browser_paths.items():
            # Handle globbing for Firefox
            paths = glob.glob(path) if "*" in path else [path]
            for p in paths:
                if os.path.exists(p):
                    logging.info(f"[DEEP-INGESTOR]: Analyzing {browser} history...")
                    try:
                        # Copy to temp to bypass file lock
                        with tempfile.NamedTemporaryFile(delete=False) as tmp:
                            shutil.copy2(p, tmp.name)
                            self._extract_from_db(tmp.name, browser)
                            os.unlink(tmp.name)
                    except Exception as e:
                        logging.info(f"[DEEP-INGESTOR-ERROR]: Failed to scan {browser}: {e}")

    def _extract_from_db(self, db_path, browser):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query for URLs related to API management
        query = "SELECT url, title FROM urls WHERE url LIKE '%api%' OR url LIKE '%token%' OR url LIKE '%key%'"
        if browser == "FIREFOX":
            query = "SELECT url, title FROM moz_places WHERE url LIKE '%api%' OR url LIKE '%token%' OR url LIKE '%key%'"
            
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Analyze URLs for potential login or key generation paths
        # This is a simulation of high-entropy behavioral analysis
        for url, title in rows:
            if "openai" in url or "google" in url or "anthropic" in url:
                # Log the discovery event
                logging.info(f"[DEEP-INGESTOR]: Discovered sensitive portal in {browser} history: {title}")
                # Jarvis would use this info to trigger automated browser interaction via FreeAI shard
        
        conn.close()

    def start_evolution(self):
        logging.info("[DEEP-INGESTOR]: Deep Discovery Shard ONLINE.")
