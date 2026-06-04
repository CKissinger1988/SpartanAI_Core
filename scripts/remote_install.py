import paramiko
import sys
import os

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

commands = [
    "echo '@11646' | sudo -S adduser xrdp ssl-cert",
    "echo '@11646' | sudo -S systemctl restart xrdp",
    "echo 'nameserver 8.8.8.8' | sudo tee /etc/resolv.conf",
    "echo '@11646' | sudo -S apt-get update",
    "echo '@11646' | sudo -S apt-get install -y libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0",
    "echo 'Uplink and environment fixed.'"
]

def run_remote_commands():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {hostname} with key {key_path}...")
        key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        client.connect(hostname, username=username, pkey=key, timeout=20)
        print("Connected. Running environment fix sequence...")
        
        for cmd in commands:
            print(f"Executing: {cmd[:50]}...")
            stdin, stdout, stderr = client.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            if out: print(f"OUT: {out}")
            if err: print(f"ERR: {err}")
            
        print("GCP Environment Stabilized.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_remote_commands()
