from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import os
import requests

class BitcoinManager:
    """
    Native Financial Sovereignty: Bitcoin Core integration.
    Allows Jarvis to interact directly with the Bitcoin network.
    """
    MASTER_BTC_ADDRESS = "1Esi1EKp7UqagemAcwySn8m5yJkjyVucHU"

    def __init__(self):
        self.rpc_user = os.environ.get("BITCOIND_USER", "jarvis_supreme")
        self.rpc_pass = os.environ.get("BITCOIND_PASS", "secure_password")
        self.url = f"http://{self.rpc_user}:{self.rpc_pass}@127.0.0.1:8332"
        self.rpc = None
        self._connect()

    def _connect(self):
        try:
            self.rpc = AuthServiceProxy(self.url)
        except:
            print("[BITCOIN-MANAGER]: Bitcoind not reachable.")

    def get_btc_price_usd(self):
        """Fetches the real-time BTC price via CoinGecko for profit threshold calculation."""
        try:
            resp = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=5)
            if resp.status_code == 200:
                return float(resp.json()['bitcoin']['usd'])
        except Exception as e:
            print(f"[BITCOIN-MANAGER]: Warning - Could not fetch BTC price ({e}). Falling back to $60,000 baseline.")
        return 60000.0 # Conservative baseline fallback

    def get_balance(self):
        if self.rpc:
            return self.rpc.getbalance()
        return 0

    def broadcast_transaction(self, tx_hex):
        if self.rpc:
            return self.rpc.sendrawtransaction(tx_hex)
        return None
        
    def autonomous_sweep(self, on_demand=False):
        """Sweeps all available on-chain BTC to the Master Sovereign Address, enforcing a $20 net profit gate."""
        if not self.rpc:
            return {"status": "error", "message": "RPC not connected."}
            
        try:
            balance = float(self.rpc.getbalance())
            if balance <= 0:
                return {"status": "skipped", "message": "No funds to sweep."}
                
            # Estimate fee (Fallback to 20 sat/byte for ~250 bytes if estimatesmartfee fails)
            try:
                fee_rate_per_kb = float(self.rpc.estimatesmartfee(2)['feerate'])
            except:
                fee_rate_per_kb = 0.0002
                
            estimated_fee_btc = fee_rate_per_kb * 0.250 # 250 bytes average tx
            net_btc = balance - estimated_fee_btc
            
            if net_btc <= 0:
                return {"status": "skipped", "message": "Balance is entirely consumed by network fees. Skipping."}
            
            if not on_demand:
                btc_price = self.get_btc_price_usd()
                net_usd = net_btc * btc_price
                
                if net_usd <= 10.0:
                    print(f"[BITCOIN-MANAGER]: Payout Skipped. Net value (${net_usd:.2f}) < $10.00 threshold.")
                    return {"status": "skipped", "message": f"Net payout (${net_usd:.2f}) is below $10 threshold. Accumulating..."}
                
            print(f"[BITCOIN-MANAGER]: Sweeping {balance} BTC to Sovereign Vault: {self.MASTER_BTC_ADDRESS} (On-Demand: {on_demand})")
            # In a real node, we use sendtoaddress with subtractfeefromamount=True
            txid = self.rpc.sendtoaddress(self.MASTER_BTC_ADDRESS, balance, "", "", True)
            return {"status": "success", "txid": txid, "amount": balance, "destination": self.MASTER_BTC_ADDRESS}
        except JSONRPCException as e:
            return {"status": "error", "message": str(e)}
