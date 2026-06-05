import subprocess
import time
import os

lnd_dir = r"C:\GitHub\SpartanAI_Core\data\lnd"
lncli_bin = r"C:\GitHub\SpartanAI_Core\tools\lnd\lncli"
wsl_lncli = "/mnt/c/GitHub/SpartanAI_Core/tools/lnd/lncli"

password = "spartan-lnd-123"

def create_wallet():
    print("[*] Attempting to create LND wallet via WSL...")
    cmd = ["wsl", "-d", "Ubuntu-Preview", "--", "bash", "-c", 
           f"{wsl_lncli} --lnddir=/mnt/c/GitHub/SpartanAI_Core/data/lnd create"]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        # Passwords
        proc.stdin.write(password + "\n")
        proc.stdin.flush()
        time.sleep(1)
        proc.stdin.write(password + "\n")
        proc.stdin.flush()
        time.sleep(1)
        # Seed? n
        proc.stdin.write("n\n")
        proc.stdin.flush()
        time.sleep(1)
        # Passphrase? n
        proc.stdin.write("n\n")
        proc.stdin.flush()
        
        stdout, stderr = proc.communicate(timeout=30)
        print(stdout)
        print(stderr)
    except Exception as e:
        print(f"[!] Error: {e}")
        proc.kill()

if __name__ == "__main__":
    create_wallet()
