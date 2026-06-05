import paramiko
import sys
import os

hostname = "136.107.205.246"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

def check_remote_status():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {hostname}...")
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        client.connect(hostname, username=username, pkey=key, timeout=20)
        
        commands = [
            "pgrep -f lms",
            "ss -tuln | grep 1234",
            "export PATH=$PATH:$HOME/.lmstudio/bin; lms ps"
        ]
        
        results = {}
        for cmd in commands:
            stdin, stdout, stderr = client.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            out = stdout.read().decode().strip()
            results[cmd] = {"out": out, "exit": exit_status}
            
        print("\n--- GCP Cognitive Node Status ---")
        lms_proc = "ACTIVE" if results["pgrep -f lms"]["exit"] == 0 else "OFFLINE"
        port_1234 = "LISTENING" if results["ss -tuln | grep 1234"]["out"] else "CLOSED"
        
        print(f"LM-Studio Process : {lms_proc}")
        print(f"API Port (1234)   : {port_1234}")
        print(f"Active Models     :\n{results['export PATH=$PATH:$HOME/.lmstudio/bin; lms ps']['out']}")
        
    except Exception as e:
        print(f"Status check failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    check_remote_status()
