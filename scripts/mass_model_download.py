import paramiko
import sys
import os

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

models = [
    "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
    "lmstudio-community/gemma-2-9b-it-GGUF",
    "lmstudio-community/Mistral-7B-Instruct-v0.3-GGUF",
    "lmstudio-community/DeepSeek-Coder-V2-Lite-Instruct-GGUF",
    "lmstudio-community/Qwen2.5-7B-Instruct-GGUF",
    "lmstudio-community/Phi-3.5-mini-instruct-GGUF"
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
        
        print("Initiating mass cognitive model ingestion...")
        for model in models:
            print(f"Queueing download for: {model}")
            cmd = f"{lms} nohup lms get {model} -y > download_{model.split('/')[-1]}.log 2>&1 &"
            client.exec_command(cmd)
            
        print("All downloads queued successfully in the background.")
        
    finally:
        client.close()

if __name__ == "__main__":
    download_models()
