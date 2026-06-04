import paramiko
import sys
import os

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

commands = [
    f"echo '{passphrase}' | sudo -S apt-get install -y libgl1 libglx-mesa0 libegl1 libxkbcommon-x11-0 x11-apps",
    "echo 'GUI dependencies updated.'"
]

def run_remote_commands():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {hostname} with key {key_path}...")
        key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        client.connect(hostname, username=username, pkey=key, timeout=20)
        print("Connected. Running final GUI dependency fix...")
        
        for cmd in commands:
            print(f"Executing: {cmd}...")
            stdin, stdout, stderr = client.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            if out: print(f"OUT: {out}")
            if err: print(f"ERR: {err}")
            
        print("GCP Dependencies Solidified.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_remote_commands()
