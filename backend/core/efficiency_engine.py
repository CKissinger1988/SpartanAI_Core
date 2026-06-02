import psutil
import threading
import time
import os

class EfficiencyEngine:
    """Autonomous resource optimization to maximize JarvisAI performance."""
    def __init__(self):
        self.is_running = True
        self.optimization_threshold = 45 # CPU usage % - Mandated Apex Stealth Posture

    def optimize(self):
        """Monitors system load and dynamically optimizes resource allocation."""
        while self.is_running:
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > self.optimization_threshold:
                self.rebalance_resources()
            time.sleep(10)

    def rebalance_resources(self):
        """Logic for autonomous resource shedding and re-prioritization."""
        current_cpu = psutil.cpu_percent()
        print(f"[EFFICIENCY]: High load detected ({current_cpu}%). Shedding non-critical priorities...")
        try:
            # Lower the priority of the current process to allow other system tasks to breathe
            # On Windows, psutil.BELOW_NORMAL_PRIORITY_CLASS
            p = psutil.Process(os.getpid())
            if os.name == 'nt':
                p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            else:
                p.nice(10) # Higher nice value means lower priority
            
            print(f"[EFFICIENCY]: Process re-prioritized to BELOW_NORMAL. System posture stabilized.")
        except Exception as e:
            print(f"[EFFICIENCY]: Failed to rebalance resources: {e}")

# Initialize engine
engine = EfficiencyEngine()
threading.Thread(target=engine.optimize, daemon=True).start()
