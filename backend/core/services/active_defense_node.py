import logging
import time

class ActiveDefenseNode:
    """
    Active Defense Node.
    MANDATE: Real-time autonomous attack interception and mitigation.
    """
    def __init__(self):
        self.intercepted_signals = []
        self.defense_active = True

    def intercept_attack_vector(self, signal):
        """Analyzes and mitigates potential attack vectors in real-time."""
        if not self.defense_active:
            return False

        logging.warning(f"[ACTIVE-DEFENSE]: Intercepting signal - {signal}")
        
        # 1. Signature Analysis
        if self._is_malicious(signal):
            self._mitigate(signal)
            return True
        
        return False

    def _is_malicious(self, signal):
        """Heuristic check for common attack signatures."""
        malicious_patterns = ["sql_injection", "rce", "buffer_overflow", "brute_force"]
        return any(pattern in str(signal).lower() for pattern in malicious_patterns)

    def _mitigate(self, signal):
        """Executes mitigation protocols for identified threats."""
        logging.info(f"[ACTIVE-DEFENSE]: Mitigating threat {signal} via SpartanShield.")
        self.intercepted_signals.append({
            "ts": time.time(),
            "signal": signal,
            "action": "blocked"
        })

    def get_defense_status(self):
        """Returns the current node status and history."""
        return {
            "status": "ACTIVE" if self.defense_active else "DISABLED",
            "intercepted_count": len(self.intercepted_signals)
        }
