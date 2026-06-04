import paramiko
import sys
import os

hostname = "34.182.160.186"
username = "ubuntu"
passphrase = "@11646"
key_path = r"C:\GitHub\.ssh\SpartanAI-Core.pem"

def deploy_autostart():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        try:
            key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        except:
            key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
            
        client.connect(hostname, username=username, pkey=key, timeout=30)
        
        # 1. Create Daemon Service
        daemon_service = """[Unit]
Description=LM Studio Daemon
After=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
User=ubuntu
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/ubuntu/.lmstudio/bin"
ExecStart=/home/ubuntu/.lmstudio/bin/lms daemon up
[Install]
WantedBy=multi-user.target
"""
        # 2. Create Server Service
        server_service = """[Unit]
Description=LM Studio API Server
After=lms-daemon.service

[Service]
Type=oneshot
RemainAfterExit=yes
User=ubuntu
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/ubuntu/.lmstudio/bin"
ExecStart=/home/ubuntu/.lmstudio/bin/lms server start --port 1234 --bind 0.0.0.0 --cors
[Install]
WantedBy=multi-user.target
"""
        
        print("Uploading systemd service files...")
        # Write to temp files then move with sudo
        client.exec_command(f"echo '{daemon_service}' > /tmp/lms-daemon.service")
        client.exec_command(f"echo '{server_service}' > /tmp/lms-server.service")
        
        cmds = [
            "sudo mv /tmp/lms-daemon.service /etc/systemd/system/",
            "sudo mv /tmp/lms-server.service /etc/systemd/system/",
            "sudo systemctl daemon-reload",
            "sudo systemctl enable lms-daemon",
            "sudo systemctl enable lms-server",
            "sudo systemctl restart lms-daemon",
            "time.sleep(5)", # Wait for daemon
            "sudo systemctl restart lms-server"
        ]
        
        for cmd in cmds:
            if cmd == "time.sleep(5)": continue
            print(f"Executing: {cmd}...")
            stdin, stdout, stderr = client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            
        print("Autostart services deployed and enabled.")
        
    finally:
        client.close()

if __name__ == "__main__":
    deploy_autostart()
