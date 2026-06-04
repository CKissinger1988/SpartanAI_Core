import paramiko
import sys
import os
import time

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

def final_deploy():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        client.connect(hostname, username=username, pkey=key, timeout=30)
        lms = "export PATH=$PATH:$HOME/.lmstudio/bin; "
        
        print("Stopping existing server...")
        client.exec_command(f"{lms} lms server stop")
        time.sleep(2)
        
        print("Starting server on 0.0.0.0:1234 with CORS...")
        # Note: Using nohup to keep it running
        cmd = f"{lms} nohup lms server start --port 1234 --bind 0.0.0.0 --cors > lms_server.log 2>&1 &"
        client.exec_command(cmd)
        time.sleep(5)
        
        print("Loading default model (phi-3)...")
        # Attempt to load a model. If it needs download, it might take time.
        load_cmd = f"{lms} lms load lmstudio-community/Phi-3-mini-4k-instruct-gguf"
        # We don't wait for this one to finish if it's long, but lms load usually waits
        stdin, stdout, stderr = client.exec_command(load_cmd)
        
        # Give it some time to start loading
        print("Verifying port 1234 on 0.0.0.0...")
        stdin, stdout, stderr = client.exec_command("netstat -tuln | grep 1234")
        print(stdout.read().decode().strip())
        
    finally:
        client.close()

if __name__ == "__main__":
    final_deploy()
