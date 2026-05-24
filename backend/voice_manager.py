import json
import os

SETTINGS_FILE = "backend/voice_settings.json"

def get_voice_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"commands": {}, "authorizations": []}
    with open(SETTINGS_FILE, 'r') as f:
        return json.load(f)

def update_command(command_name, action, authorized_roles):
    settings = get_voice_settings()
    settings["commands"][command_name] = {
        "action": action,
        "roles": authorized_roles
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def authorize_user_voice(user_id, command_name):
    settings = get_voice_settings()
    if command_name in settings["commands"]:
        if user_id not in settings["authorizations"]:
            settings["authorizations"].append(user_id)
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=4)
            return True
    return False
