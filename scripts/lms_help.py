import paramiko
import sys
import os

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

def check_help():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        client.connect(hostname, username=username, pkey=key, timeout=30)
        lms = "export PATH=$PATH:$HOME/.lmstudio/bin; "
        stdin, stdout, stderr = client.exec_command(f"{lms} lms daemon --help")
        print(stdout.read().decode().strip())
    finally:
        client.close()

if __name__ == "__main__":
    check_help()
