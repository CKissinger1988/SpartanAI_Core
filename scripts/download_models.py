import paramiko
import sys
import os

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

models = [
    "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
    "lmstudio-community/Qwen2-7B-Instruct-GGUF",
    "lmstudio-community/Phi-3-mini-4k-instruct-gguf"
]

def download_models():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        client.connect(hostname, username=username, pkey=key, timeout=30)
        lms = "export PATH=$PATH:$HOME/.lmstudio/bin; "
        
        for model in models:
            print(f"Initiating download for: {model}...")
            # We use nohup to ensure it completes even if session drops
            cmd = f"{lms} nohup lms get {model} > download_{model.split('/')[-1]}.log 2>&1 &"
            client.exec_command(cmd)
            
        print("Model downloads initiated in background. Use 'lms ls' to check progress.")
        
    finally:
        client.close()

if __name__ == "__main__":
    download_models()
