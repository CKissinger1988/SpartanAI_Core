import sys
import os
import ctypes
import platform
import logging

logger = logging.getLogger("GhostIntegrity")

def enforce_anti_debug():
    """Detects if a debugger is attached and terminates if found."""
    if platform.system() == "Windows":
        # Check for IsDebuggerPresent on Windows
        if ctypes.windll.kernel32.IsDebuggerPresent():
            logger.critical("[GHOST] Debugger detected. Self-terminating for security.")
            sys.exit(1)
    elif platform.system() == "Linux":
        # Check for TracerPid in /proc/self/status on Linux
        try:
            with open("/proc/self/status", "r") as f:
                for line in f:
                    if line.startswith("TracerPid:") and int(line.split()[1]) != 0:
                        logger.critical("[GHOST] Linux Tracer detected. Self-terminating.")
                        sys.exit(1)
        except Exception:
            pass # Procfs may not be available in some environments

def secure_clear_memory(obj):
    """Overwrites sensitive data in memory before deletion (Simulated)."""
    # In Python, we can't easily clear raw memory due to immutability and GC,
    # but we can overwrite mutable types or clear references.
    if isinstance(obj, bytearray):
        for i in range(len(obj)):
            obj[i] = 0
    del obj

def verify_code_integrity():
    """Verify script signatures or checksums (Placeholder)."""
    # This would check the hash of the running script against a known good value
    pass
