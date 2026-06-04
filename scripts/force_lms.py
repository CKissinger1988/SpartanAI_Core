import paramiko
import sys
import os
import time

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

def force_deploy():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {hostname}...")
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        client.connect(hostname, username=username, pkey=key, timeout=30)
        
        lms = "export PATH=$PATH:$HOME/.lmstudio/bin; "
        
        print("Starting server explicitly...")
        # Try to start server on all interfaces if possible
        client.exec_command(f"{lms} lms server stop")
        time.sleep(2)
        # Some versions of lms server start don't have --host, they use default
        stdin, stdout, stderr = client.exec_command(f"{lms} lms server start --port 1234")
        
        # Capture some output to see if it's blocking or what
        time.sleep(5)
        out = stdout.read(1000).decode().strip()
        print(f"Server Output: {out}")
        
        print("Checking port 1234...")
        stdin, stdout, stderr = client.exec_command("sudo lsof -i :1234")
        print(stdout.read().decode().strip())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    force_deploy()
