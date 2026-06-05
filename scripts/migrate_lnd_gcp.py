import paramiko
import os
import sys

# SUPREME MIGRATION ENGINE
# MANDATE: Port LND node to GCP for 24/7 cloud persistence.

hostname = "136.107.205.246"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

LND_BIN = r"C:\GitHub\SpartanAI_Core\tools\lnd\lnd"
LNCLI_BIN = r"C:\GitHub\SpartanAI_Core\tools\lnd\lncli"
LND_CONF = r"C:\GitHub\SpartanAI_Core\data\lnd\lnd.conf"

REMOTE_LND_DIR = "/home/ubuntu/spartan/lnd"

def migrate_lnd():
    print(f"[*] Initiating Exodus sequence to {hostname}...")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        client.connect(hostname, username=username, pkey=key, timeout=30)
        
        # 1. Create directory structure
        print("[*] Creating remote infrastructure...")
        client.exec_command(f"mkdir -p {REMOTE_LND_DIR}")
        
        # 2. SFTP Upload
        sftp = client.open_sftp()
        
        print("[*] Porting LND Binaries (this may take a moment)...")
        sftp.put(LND_BIN, f"{REMOTE_LND_DIR}/lnd")
        sftp.put(LNCLI_BIN, f"{REMOTE_LND_DIR}/lncli")
        
        print("[*] Porting Configuration...")
        sftp.put(LND_CONF, f"{REMOTE_LND_DIR}/lnd.conf")
        
        sftp.close()
        
        # 3. Finalize Permissions and Start
        print("[*] Finalizing remote execution environment...")
        client.exec_command(f"chmod +x {REMOTE_LND_DIR}/lnd {REMOTE_LND_DIR}/lncli")
        
        # Launch LND on GCP
        start_cmd = f"nohup {REMOTE_LND_DIR}/lnd --lnddir={REMOTE_LND_DIR} --configfile={REMOTE_LND_DIR}/lnd.conf > {REMOTE_LND_DIR}/lnd.log 2>&1 &"
        client.exec_command(start_cmd)
        
        print("[SUCCESS] Exodus sequence complete. LND is now cloud-persistent.")
        
    except Exception as e:
        print(f"[!] Migration Failure: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    migrate_lnd()
