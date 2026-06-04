import paramiko
import sys
import os

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

def read_remote_logs():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {hostname}...")
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        client.connect(hostname, username=username, pkey=key, timeout=20)
        
        log_files = ["lms_daemon.log", "lms_server.log"]
        for log in log_files:
            print(f"\n--- {log} ---")
            stdin, stdout, stderr = client.exec_command(f"tail -n 20 {log}")
            print(stdout.read().decode().strip())
            
        print("\n--- Listing models ---")
        stdin, stdout, stderr = client.exec_command("export PATH=$PATH:$HOME/.lmstudio/bin; lms ls")
        print(stdout.read().decode().strip())
        
    except Exception as e:
        print(f"Failed to read logs: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    read_remote_logs()
