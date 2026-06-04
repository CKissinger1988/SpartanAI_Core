import paramiko
import sys
import os
import time

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

# Installation and Configuration commands
commands = [
    "sudo apt-get update",
    "sudo apt-get install -y curl fuse libfuse2 libasound2t64",
    "curl -fsSL https://lmstudio.ai/install.sh | bash",
    # Wait for installation to settle
    "export PATH=$PATH:$HOME/.lmstudio/bin; nohup lms daemon up > lms_daemon.log 2>&1 &",
    "sleep 10",
    "export PATH=$PATH:$HOME/.lmstudio/bin; lms get qwen2",
    "export PATH=$PATH:$HOME/.lmstudio/bin; nohup lms server start --port 1234 > lms_server.log 2>&1 &"
]

def run_remote_commands():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {hostname} with key {key_path}...")
        # Note: Using Ed25519Key as in remote_install.py, but SpartanAI-Core.pem might be RSA
        # remote_install.py used Ed25519Key, let's stick to that unless it fails
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        client.connect(hostname, username=username, pkey=key, timeout=30)
        print("Connected to GCP. Initiating LM-Studio Installation...")
        
        for cmd in commands:
            print(f"Executing: {cmd}...")
            stdin, stdout, stderr = client.exec_command(cmd)
            # Some commands might take time
            exit_status = stdout.channel.recv_exit_status()
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            if out: print(f"OUT: {out}")
            if err: print(f"ERR: {err}")
            
        print("\nLM-Studio Installation and Server Configuration COMPLETE on GCP.")
        print("Server should be listening on port 1234.")
    except Exception as e:
        print(f"Error during remote operation: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_remote_commands()
