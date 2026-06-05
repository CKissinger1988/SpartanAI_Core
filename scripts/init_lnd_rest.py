import requests
import json
import base64
import os

url = "https://127.0.0.1:8080/v1/genseed"

def init_wallet():
    print("[*] Generating seed via REST...")
    try:
        resp = requests.get(url, timeout=10, verify=False)
        if resp.status_code != 200:
            print(f"[!] Error generating seed: {resp.text}")
            return
        
        seed_data = resp.json()
        cipher_seed = seed_data['cipher_seed_mnemonic']
        print(f"[+] Seed generated (24 words).")
        
        # Save seed for the creator
        seed_path = r"C:\GitHub\SpartanAI_Core\data\lnd\seed.txt"
        with open(seed_path, "w") as f:
            f.write("\n".join(cipher_seed))
        print(f"[*] Seed saved to {seed_path}")
        
        init_url = "https://127.0.0.1:8080/v1/initwallet"
        payload = {
            "wallet_password": base64.b64encode(b"spartan123").decode(),
            "cipher_seed_mnemonic": cipher_seed
        }
        
        print("[*] Initializing wallet via REST...")
        resp = requests.post(init_url, json=payload, timeout=30, verify=False)
        if resp.status_code == 200:
            print("[SUCCESS] Wallet initialized successfully.")
        else:
            print(f"[!] Error initializing wallet: {resp.text}")
            
    except Exception as e:
        print(f"[!] Critical failure: {e}")

if __name__ == "__main__":
    init_wallet()
