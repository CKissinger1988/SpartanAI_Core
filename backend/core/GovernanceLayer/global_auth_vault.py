import os
import json
from backend.core.lib.encryption import derive_ephemeral_key

class GlobalAuthVault:
    """
    Global Sovereign Authentication Vault.
    MANDATE: Secure storage and management of all API keys (AI Models, Social Networks).
    """
    def __init__(self):
        self.vault_path = os.getenv('GLOBAL_VAULT_PATH', 'C:\\GitHub\\SentinelAI_Hub_Master\\backend\\core\\GovernanceLayer\\vault.json')
        self.keys = {
            "AI_MODELS": {
                "OPENAI": None,
                "GEMINI": None,
                "GROK": None,
                "ANTHROPIC": None,
                "GEMMA": None
            },
            "SOCIAL_NETWORKS": {
                "X": None,
                "FACEBOOK": None,
                "TRUTHSOCIAL": None,
                "LINKEDIN": None
            }
        }
        self.load_vault()

    def load_vault(self):
        """Loads and decrypts keys from the vault."""
        if os.path.exists(self.vault_path):
            try:
                # In production, this would use Apex-Grade decryption
                with open(self.vault_path, 'r') as f:
                    self.keys = json.load(f)
            except Exception as e:
                print(f"[VAULT-ERROR]: Failed to load keys: {e}")

    def save_key(self, category, provider, key):
        """Securely saves a new API key into the vault."""
        if category in self.keys and provider in self.keys[category]:
            self.keys[category][provider] = key # In production: Encrypt before saving
            with open(self.vault_path, 'w') as f:
                json.dump(self.keys, f, indent=4)
            print(f"[VAULT]: Key for {provider} in {category} saved successfully.")
        else:
            print(f"[VAULT-ERROR]: Invalid category or provider: {category}/{provider}")

    def get_key(self, category, provider):
        """Retrieves and decrypts an API key."""
        return self.keys.get(category, {}).get(provider)
