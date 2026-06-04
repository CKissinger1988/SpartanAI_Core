import paramiko
import sys
import os

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

def check_reachability():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        client.connect(hostname, username=username, pkey=key, timeout=30)
        
        print("Checking server reachability via curl on remote host...")
        stdin, stdout, stderr = client.exec_command("curl -s http://127.0.0.1:1234/v1/models")
        print(f"Local curl: {stdout.read().decode().strip()}")
        
        # Check external bind
        stdin, stdout, stderr = client.exec_command("curl -s http://34.182.160.186:1234/v1/models")
        print(f"External IP curl: {stdout.read().decode().strip()}")
        
    finally:
        client.close()

if __name__ == "__main__":
    check_reachability()
