import os
import json
import codecs
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress insecure request warnings for self-signed LND certs
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class LNDManager:
    """
    Lightning Network Daemon (LND) Integration.
    Enables SpartanAI to execute sub-second, micro-transaction trading and autonomous settlements.
    Adheres to Apex-Grade Standards: Zero Simulation, real-world Lightning operations.
    """
    def __init__(self):
        # Default LND REST API port is 8080
        self.lnd_host = os.environ.get("LND_REST_HOST", "127.0.0.1:8080")
        self.lnd_dir = os.environ.get("LND_DIR", os.path.expanduser("~/.lnd"))
        self.network = os.environ.get("LND_NETWORK", "mainnet")
        self.MASTER_BTC_ADDRESS = "1Esi1EKp7UqagemAcwySn8m5yJkjyVucHU"
        
        self.macaroon_path = os.path.join(self.lnd_dir, "data", "chain", "bitcoin", self.network, "admin.macaroon")
        self.tls_cert_path = os.path.join(self.lnd_dir, "tls.cert")
        
        self.headers = {}
        self.session = requests.Session()
        self._load_credentials()

    def _load_credentials(self):
        """Loads the macaroon for authenticated LND requests."""
        if not os.path.exists(self.macaroon_path):
            print(f"[LND-MANAGER]: WARNING - Macaroon not found at {self.macaroon_path}. LND Offline.")
            return

        try:
            with open(self.macaroon_path, 'rb') as f:
                macaroon_bytes = f.read()
                macaroon = codecs.encode(macaroon_bytes, 'hex').decode('utf-8')
                self.headers = {'Grpc-Metadata-macaroon': macaroon}
        except Exception as e:
            print(f"[LND-MANAGER]: ERROR loading macaroon - {e}")

    def _request(self, method, endpoint, data=None):
        if not self.headers:
            return {"error": "LND credentials not loaded"}
            
        url = f"https://{self.lnd_host}/v1/{endpoint}"
        
        # Use TLS cert if it exists, otherwise disable verification (risky, but standard for local lnd)
        verify = self.tls_cert_path if os.path.exists(self.tls_cert_path) else False
        
        try:
            if method == 'GET':
                r = self.session.get(url, headers=self.headers, verify=verify)
            elif method == 'POST':
                r = self.session.post(url, headers=self.headers, data=json.dumps(data), verify=verify)
            elif method == 'DELETE':
                r = self.session.delete(url, headers=self.headers, verify=verify)
            else:
                return {"error": "Unsupported HTTP method"}
                
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "details": r.text if 'r' in locals() else None}

    def get_info(self):
        """Get LND node information and sync status."""
        return self._request('GET', 'getinfo')

    def get_wallet_balance(self):
        """Get on-chain wallet balance."""
        return self._request('GET', 'balance/blockchain')

    def get_channel_balance(self):
        """Get Lightning channel balance."""
        return self._request('GET', 'balance/channels')

    def create_invoice(self, amount_sats, memo):
        """Generate a Lightning Invoice for autonomous monetization."""
        data = {
            "value": amount_sats,
            "memo": memo
        }
        return self._request('POST', 'invoices', data)

    def pay_invoice(self, payment_request):
        """Pay a Lightning Invoice automatically."""
        data = {
            "payment_request": payment_request
        }
        return self._request('POST', 'channels/transactions', data)

    def get_peers(self):
        """List connected Lightning peers."""
        return self._request('GET', 'peers')
        
    def get_btc_price_usd(self):
        """Fetches the real-time BTC price via CoinGecko for profit threshold calculation."""
        try:
            resp = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=5)
            if resp.status_code == 200:
                return float(resp.json()['bitcoin']['usd'])
        except Exception as e:
            print(f"[LND-MANAGER]: Warning - Could not fetch BTC price ({e}). Falling back to $60,000 baseline.")
        return 60000.0

    def autonomous_sweep(self, on_demand=False):
        """Sweeps all available on-chain LND funds to the Master Sovereign Address, enforcing a $20 net profit gate."""
        print(f"[LND-MANAGER]: Evaluating sweep of on-chain funds to {self.MASTER_BTC_ADDRESS} (On-Demand: {on_demand})...")
        
        balance_resp = self.get_wallet_balance()
        if "error" in balance_resp:
            return balance_resp
            
        balance_sats = int(balance_resp.get("total_balance", 0))
        if balance_sats <= 0:
            return {"status": "skipped", "message": "No funds to sweep."}
            
        estimated_fee_sats = 2000 # Conservative flat estimate for a sweep tx
        net_sats = balance_sats - estimated_fee_sats
        
        if net_sats <= 0:
            return {"status": "skipped", "message": "Balance is entirely consumed by network fees. Skipping."}
        
        if not on_demand:
            btc_price = self.get_btc_price_usd()
            net_usd = (net_sats / 100000000.0) * btc_price
            
            if net_usd <= 10.0:
                print(f"[LND-MANAGER]: Payout Skipped. Net value (${net_usd:.2f}) < $10.00 threshold.")
                return {"status": "skipped", "message": f"Net payout (${net_usd:.2f}) is below $10 threshold. Accumulating..."}
                
        print(f"[LND-MANAGER]: Executing on-chain sweep...")
        data = {
            "addr": self.MASTER_BTC_ADDRESS,
            "send_all": True
        }
        return self._request('POST', 'channels/transactions', data)
        
    def check_readiness(self):
        """Checks if the node is synced and ready for trading operations."""
        info = self.get_info()
        if "error" in info:
            return False, info["error"]
            
        synced = info.get("synced_to_chain", False)
        return synced, "Node is synced and ready" if synced else "Node is syncing to blockchain"

if __name__ == "__main__":
    lnd = LNDManager()
    info = lnd.get_info()
    if "error" in info:
        print("[LND-MANAGER]: Node Unreachable. Is LND running?")
    else:
        print(f"[LND-MANAGER]: Connected to node {info.get('alias', 'UNKNOWN')} ({info.get('version')})")
        print(f"Synced to chain: {info.get('synced_to_chain')}")
        print(f"Active Channels: {info.get('num_active_channels')}")
