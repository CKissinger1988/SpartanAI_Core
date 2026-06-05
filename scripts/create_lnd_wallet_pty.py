import subprocess
import os
import pty
import time

lnd_bin = "/mnt/c/GitHub/SpartanAI_Core/tools/lnd/lncli"
lnd_dir = "/mnt/c/GitHub/SpartanAI_Core/data/lnd"
password = b"spartan-lnd-123\n"

def master_read(fd):
    data = os.read(fd, 1024)
    return data

def create_wallet():
    print("[*] Spawning PTY for LND wallet creation...")
    pid, fd = pty.fork()
    
    if pid == 0: # Child
        os.execv(lnd_bin, [lnd_bin, "--lnddir=" + lnd_dir, "create"])
    else: # Parent
        time.sleep(2)
        os.write(fd, password) # Pass 1
        time.sleep(1)
        os.write(fd, password) # Pass 2
        time.sleep(1)
        os.write(fd, b"n\n") # Seed
        time.sleep(1)
        os.write(fd, b"n\n") # Passphrase
        
        # Read output for a bit
        for _ in range(10):
            try:
                out = os.read(fd, 1024).decode()
                print(out, end="")
                if "successfully created" in out.lower():
                    break
            except: break
            time.sleep(1)

if __name__ == "__main__":
    create_wallet()
