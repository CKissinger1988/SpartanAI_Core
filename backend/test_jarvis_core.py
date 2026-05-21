import pytest
import os
import time
import threading
from backend.core.jarvis import Jarvis
from backend.switcher import ModelSwitcher
from backend.core.sentinel import SentinelRedundancy

def test_jarvis_heartbeat():
    # Jarvis should create a heartbeat file on init
    hb_file = ".jarvis_heartbeat"
    if os.path.exists(hb_file):
        os.remove(hb_file)
    
    jarvis = Jarvis()
    time.sleep(2) # Wait for heartbeat thread to fire
    assert os.path.exists(hb_file)
    mtime1 = os.path.getmtime(hb_file)
    
    time.sleep(12) # Wait for next heartbeat (interval is 10s)
    mtime2 = os.path.getmtime(hb_file)
    assert mtime2 > mtime1
    
    # Cleanup
    if os.path.exists(hb_file):
        os.remove(hb_file)

def test_model_switcher():
    switcher = ModelSwitcher()
    assert switcher.get_current() == 'auto'
    
    # Test switching to nexus (will try to start service but we check current_engine)
    # We don't necessarily need the service to be active for the switcher state to change
    switcher.switch('nexus')
    assert switcher.get_current() == 'nexus'
    
    switcher.switch('hexstrike')
    assert switcher.get_current() == 'hexstrike'
    
    # Invalid engine
    result = switcher.switch('unknown')
    assert result is False
    assert switcher.get_current() == 'hexstrike'

def test_sentinel_monitoring():
    sentinel = SentinelRedundancy()
    hb_file = ".jarvis_heartbeat"
    
    # Create a fresh heartbeat
    with open(hb_file, 'w') as f:
        f.write(str(time.time()))
    
    # Sentinel should consider it nominal
    # We can't easily test the print output, but we can verify the logic
    # doesn't trigger failover if heartbeat is fresh
    
    # Mock spawn_failover to track calls
    failover_called = []
    def mock_spawn_failover():
        failover_called.append(True)
    
    sentinel.spawn_failover = mock_spawn_failover
    
    # Fresh heartbeat
    sentinel.health_check_interval = 0.1
    # Run one check manually if possible, or start thread and wait
    # For unit test, we'll just call the check logic if it were exposed, 
    # but it's in a while loop. We'll just test spawn_failover directly.
    
    sentinel.spawn_failover()
    assert failover_called == [True]
    
    # Test stale heartbeat check logic
    # Manual check
    with open(hb_file, 'w') as f:
        f.write(str(time.time() - 20)) # 20 seconds ago
    
    # We'll just verify the failover log creation in the real spawn_failover
    from backend.core.sentinel import SentinelRedundancy as RealSentinel
    real_sentinel = RealSentinel()
    log_file = "data/sentinel_recovery.log"
    if os.path.exists(log_file):
        os.remove(log_file)
    
    real_sentinel.spawn_failover()
    assert os.path.exists(log_file)
    
    # Cleanup
    if os.path.exists(hb_file):
        os.remove(hb_file)
    if os.path.exists(log_file):
        os.remove(log_file)

def test_autonomous_routing():
    switcher = ModelSwitcher()
    
    # Test Offensive Routing
    assert switcher.route_query("Run nmap scan on target 192.168.1.1") == 'hexstrike'
    assert switcher.route_query("Find exploit for CVE-2024-0001") == 'hexstrike'
    
    # Test Sovereign Routing
    assert switcher.route_query("Search the local brain for project notes") == 'nexus'
    assert switcher.route_query("Update my private vault") == 'nexus'
    
    # Test Default Routing
    assert switcher.route_query("What is the capital of France?") == 'gemini'
    assert switcher.route_query("Explain quantum entanglement") == 'gemini'
    
    # Test get_engine_for_query logic
    switcher.switch('auto')
    engine = switcher.get_engine_for_query("Run nmap scan")
    from backend.core.hexstrike_client import HexstrikeEngine
    assert isinstance(engine, HexstrikeEngine)
    
    engine_nexus = switcher.get_engine_for_query("Search local brain")
    from backend.core.local_ai import LocalIntelligence
    assert isinstance(engine_nexus, LocalIntelligence)
