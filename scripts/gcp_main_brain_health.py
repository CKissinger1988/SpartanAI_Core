import paramiko
import sys

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

def check_main_brain_health():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        print(f"Establishing secure uplink to Main Brain ({hostname})...")
        client.connect(hostname, username=username, pkey=key, timeout=30)
        
        commands = {
            "Disk Space": "df -h /",
            "Memory Usage": "free -m",
            "System Load": "uptime",
            "LM-Studio Models": "export PATH=$PATH:$HOME/.lmstudio/bin; lms ls",
            "Daemon Status": "systemctl is-active lms-daemon",
            "Server Status": "systemctl is-active lms-server"
        }
        
        print("\n=== MAIN BRAIN (GCP) HEALTH REPORT ===")
        for name, cmd in commands.items():
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read().decode().strip()
            print(f"\n[{name}]:\n{out}")
            
    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to connect to Main Brain: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    check_main_brain_health()
