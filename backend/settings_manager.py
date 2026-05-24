import json
import os

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), 'settings.json')

def load_settings():
    """Loads tactical settings from settings.json."""
    if not os.path.exists(SETTINGS_PATH):
        return {}
    with open(SETTINGS_PATH, 'r') as f:
        return json.load(f)

def save_settings(settings):
    """Saves updated tactical settings."""
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

def get_setting(path, default=None):
    """Retrieves a specific setting using a dot-notation path (e.g., 'security.two_fa_required')."""
    settings = load_settings()
    parts = path.split('.')
    for part in parts:
        if isinstance(settings, dict) and part in settings:
            settings = settings[part]
        else:
            return default
    return settings

if __name__ == "__main__":
    print(f"Jarvis SETTINGS MANAGER ACTIVE. VERSION: {get_setting('Jarvis_version')}")
    print(f"MASTER OPERATOR: {get_setting('operator_identity')}")
