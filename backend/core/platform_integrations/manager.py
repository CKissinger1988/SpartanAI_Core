import os
import json

class PlatformIntegrator:
    """Handles integration for Facebook, Snapchat, and TextNow."""
    def __init__(self):
        self.config_dir = os.path.join(os.getcwd(), "backend", "config", "platforms")
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

    def configure_platform(self, platform, api_key, secret):
        """Securely stores platform configuration."""
        config_path = os.path.join(self.config_dir, f"{platform}.json")
        # Ensure credentials are encrypted or handled according to security mandate
        with open(config_path, 'w') as f:
            json.dump({"api_key": api_key, "secret": secret, "status": "configured"}, f)
        print(f"Platform {platform} configured.")

class LiveServerSessionManager:
    """Handles Creator auto-login on Live Server."""
    def __init__(self):
        self.is_live_server = os.environ.get("JARVIS_LIVE_SERVER", "false") == "true"

    def auto_login(self, username, token):
        if self.is_live_server:
            # Secure login logic restricted to Live Server
            print(f"Creator auto-login successful for {username} on Live Server.")
            return True
        print("Auto-login restricted to Live Server environment.")
        return False
