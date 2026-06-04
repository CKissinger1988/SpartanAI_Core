import paramiko
import sys
import os
import time

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

def deploy_lms_server():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {hostname}...")
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        client.connect(hostname, username=username, pkey=key, timeout=30)
        
        # 1. Kill any existing server attempts
        print("Cleaning up existing processes...")
        client.exec_command("pkill -f 'lms server'")
        
        # 2. Start the server
        print("Starting LM-Studio Server on port 1234...")
        lms_path = "export PATH=$PATH:$HOME/.lmstudio/bin; "
        cmd = f"{lms_path} nohup lms server start --port 1234 > lms_server.log 2>&1 &"
        client.exec_command(cmd)
        
        # 3. Wait and check
        time.sleep(10)
        stdin, stdout, stderr = client.exec_command("netstat -tuln | grep 1234")
        out = stdout.read().decode().strip()
        
        if out:
            print(f"SUCCESS: Server is listening on 1234.\n{out}")
        else:
            print("FAILURE: Server failed to bind to port 1234. Checking logs...")
            stdin, stdout, stderr = client.exec_command("tail -n 10 lms_server.log")
            print(stdout.read().decode().strip())
            
    except Exception as e:
        print(f"Deployment failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    deploy_lms_server()
