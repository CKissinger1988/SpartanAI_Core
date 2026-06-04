import paramiko
import sys
import os
import time

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

def force_server():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        client.connect(hostname, username=username, pkey=key, timeout=30)
        lms = "export PATH=$PATH:$HOME/.lmstudio/bin; export LMS_SERVER_HOST=0.0.0.0; "
        
        print("Checking downloaded models...")
        stdin, stdout, stderr = client.exec_command(f"{lms} lms ls")
        print(stdout.read().decode().strip())
        
        print("Restarting server with LMS_SERVER_HOST=0.0.0.0...")
        client.exec_command(f"{lms} lms server stop")
        time.sleep(2)
        client.exec_command(f"{lms} lms server start --port 1234")
        time.sleep(5)
        
        print("Checking bind address...")
        stdin, stdout, stderr = client.exec_command("sudo netstat -tulnp | grep 1234")
        print(stdout.read().decode().strip())
        
    finally:
        client.close()

if __name__ == "__main__":
    force_server()
