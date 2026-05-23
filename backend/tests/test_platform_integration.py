import pytest
from backend.core.platform_integrations.manager import LiveServerSessionManager

def test_auto_login_on_live_server():
    # Simulate Live Server environment
    import os
    os.environ["JARVIS_LIVE_SERVER"] = "true"
    manager = LiveServerSessionManager()
    assert manager.auto_login("Creator", "token") == True

def test_auto_login_denied_on_dev():
    # Simulate Dev environment
    import os
    os.environ["JARVIS_LIVE_SERVER"] = "false"
    manager = LiveServerSessionManager()
    assert manager.auto_login("Creator", "token") == False
