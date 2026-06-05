import paramiko
import json
import base64
import time

# REMOTE LND INITIALIZER
# MANDATE: Activate Financial Cortex on GCP node.

hostname = "136.107.205.246"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

def remote_init():
    print(f"[*] Connecting to {hostname} for remote LND initialization...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        client.connect(hostname, username=username, pkey=key, timeout=30)
        
        # 1. Generate Seed
        print("[*] Generating remote cipher seed...")
        cmd_seed = "curl -s -k -X GET https://localhost:8080/v1/genseed"
        stdin, stdout, stderr = client.exec_command(cmd_seed)
        seed_resp = stdout.read().decode().strip()
        
        if not seed_resp:
            print("[!] Error: No response from LND REST API.")
            return

        seed_data = json.loads(seed_resp)
        cipher_seed = seed_data['cipher_seed_mnemonic']
        print(f"[+] Remote seed generated.")
        
        # Save seed to local .ssh folder for safety
        with open(r"C:\GitHub\.ssh\GCP_LND_SEED.txt", "w") as f:
            f.write("\n".join(cipher_seed))
        print("[*] Remote seed backed up to C:/GitHub/.ssh/GCP_LND_SEED.txt")
        
        # 2. Initialize Wallet
        print("[*] Initializing remote wallet...")
        wallet_password_b64 = base64.b64encode(b"spartan123").decode()
        init_payload = {
            "wallet_password": wallet_password_b64,
            "cipher_seed_mnemonic": cipher_seed
        }
        
        # Construct curl command with JSON payload
        # We escape single quotes for bash
        payload_json = json.dumps(init_payload).replace("'", "'\\''")
        cmd_init = f"curl -s -k -X POST https://localhost:8080/v1/initwallet -d '{payload_json}'"
        
        stdin, stdout, stderr = client.exec_command(cmd_init)
        init_resp = stdout.read().decode().strip()
        
        print(f"[+] Remote Response: {init_resp}")
        
        # 3. Wait for macaroon generation
        print("[*] Waiting for remote finalization...")
        time.sleep(5)
        
        # 4. Verify macaroons
        stdin, stdout, stderr = client.exec_command("ls /home/ubuntu/spartan/lnd/data/chain/bitcoin/mainnet/*.macaroon")
        print(f"[*] Remote Macaroons: {stdout.read().decode().strip()}")
        
    except Exception as e:
        print(f"[!] Critical Failure: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    remote_init()
