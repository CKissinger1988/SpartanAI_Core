import requests
import json
import base64
import os

url = "https://127.0.0.1:8080/v1/unlockwallet"
password = base64.b64encode(b"spartan123").decode()

def unlock_wallet():
    print("[*] Attempting to unlock LND wallet via REST...")
    payload = {
        "wallet_password": password
    }
    try:
        resp = requests.post(url, json=payload, timeout=10, verify=False)
        if resp.status_code == 200:
            print("[SUCCESS] Wallet unlocked successfully.")
        else:
            # Check if already unlocked
            if "wallet already unlocked" in resp.text:
                print("[INFO] Wallet is already unlocked.")
            else:
                print(f"[!] Error unlocking wallet: {resp.text}")
    except Exception as e:
        print(f"[!] Failure: {e}")

if __name__ == "__main__":
    unlock_wallet()
