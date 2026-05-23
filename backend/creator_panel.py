import json
import os

PANEL_SETTINGS = "backend/creator_panel.json"

def get_system_state():
    if not os.path.exists(PANEL_SETTINGS):
        return {"features": {}, "status": "active"}
    with open(PANEL_SETTINGS, 'r') as f:
        return json.load(f)

def toggle_feature(feature_name, state):
    state_data = get_system_state()
    state_data["features"][feature_name] = state
    with open(PANEL_SETTINGS, 'w') as f:
        json.dump(state_data, f, indent=4)

def get_active_features():
    data = get_system_state()
    return [k for k, v in data["features"].items() if v]
