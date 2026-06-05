import os
import sys
import json

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.lnd_manager import LNDManager

def test_lnd():
    print("--- SpartanAI // LND Connectivity Test ---")
    lnd = LNDManager()
    
    print(f"Targeting host: {lnd.lnd_host}")
    print(f"Macaroon path: {lnd.macaroon_path}")
    
    if not os.path.exists(lnd.macaroon_path):
        print("ERROR: Macaroon file not found. Node is logically offline.")
        return

    info = lnd.get_info()
    if "error" in info:
        print(f"ERROR: Could not connect to LND REST API.")
        print(f"Message: {info.get('error')}")
        print(f"Details: {info.get('details')}")
    else:
        print(f"SUCCESS: Connected to LND node.")
        print(f"Alias: {info.get('alias')}")
        print(f"Version: {info.get('version')}")
        print(f"Synced to Chain: {info.get('synced_to_chain')}")
        print(f"Active Channels: {info.get('num_active_channels')}")
        
        balance = lnd.get_wallet_balance()
        print(f"Wallet Balance (Total): {balance.get('total_balance', '0')} sats")

if __name__ == "__main__":
    test_lnd()
