import pytest
import os
import sys
from backend.core.antigravity_bridge import AntigravityBridge

# Mock the subprocess.run to avoid needing the actual binary
import unittest.mock as mock

class TestAntigravityBridge:
    def test_init_path_detection(self):
        bridge = AntigravityBridge()
        assert bridge is not None
        # Basic check that it doesn't crash on init

    @mock.patch("subprocess.run")
    def test_run_command_success(self, mock_run):
        # Mocking the AGY path check
        with mock.patch("os.path.exists", return_value=True):
            bridge = AntigravityBridge()
            mock_run.return_value = mock.Mock(returncode=0, stdout="Success")
            
            result = bridge.run_command("test prompt")
            assert result["status"] == "success"
            assert result["data"] == "Success"

    @mock.patch("subprocess.run")
    def test_run_command_failure(self, mock_run):
        with mock.patch("os.path.exists", return_value=True):
            bridge = AntigravityBridge()
            mock_run.return_value = mock.Mock(returncode=1, stderr="Error")
            
            result = bridge.run_command("test prompt")
            assert result["status"] == "error"
            assert result["message"] == "Error"
