import subprocess
import os
import sys

class ApexLink:
    """Master Remote Access & Recovery (IAP Tunneling & Failsafes)."""
    
    def __init__(self, instance_name, project_id, zone):
        self.instance = instance_name
        self.project = project_id
        self.zone = zone
        self.gcloud_path = "/home/pentester/google-cloud-sdk/bin/gcloud"

    def connect_iap(self):
        """Method 1: Identity-Aware Proxy (IAP) Tunneling via WSL."""
        print(f"[*] Establishing Apex Ghost Link to {self.instance} via IAP Tunnel (WSL)...")
        # Construct the WSL command
        wsl_cmd = [
            "wsl", "-d", "kali-linux", "bash", "-c",
            f"'{self.gcloud_path}' compute ssh {self.instance} --tunnel-through-iap --project={self.project} --zone={self.zone}"
        ]
        try:
            # Note: This will be interactive for the user
            subprocess.run(wsl_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[!] IAP Connection Failed: {e}")
            return False
        return True

    def enable_serial_console(self):
        """Failsafe 1: Enable Serial Port Access for Emergency Console."""
        print(f"[*] Hardening Failsafe: Enabling Serial Console on {self.instance}...")
        # Note: Failsafes also use the WSL gcloud path for consistency
        wsl_cmd = [
            "wsl", "-d", "kali-linux", "bash", "-c",
            f"'{self.gcloud_path}' compute instances add-metadata {self.instance} --metadata serial-port-enable=true --project={self.project} --zone={self.zone}"
        ]
        return subprocess.run(wsl_cmd, capture_output=True).returncode == 0

    def autonomous_firewall_recovery(self):
        """Failsafe 2: Update firewall to allow current public IP (Self-Healing)."""
        import requests
        try:
            current_ip = requests.get("https://checkip.amazonaws.com", timeout=5).text.strip()
            print(f"[*] Self-Healing: Whitelisting current IP {current_ip} in GCP Firewall...")
            
            # Rule name follows SpartanAI naming convention
            rule_name = "spartan-sovereign-recovery"
            
            # Check if rule exists or create/update
            wsl_cmd_update = [
                "wsl", "-d", "kali-linux", "bash", "-c",
                f"'{self.gcloud_path}' compute firewall-rules update {rule_name} --source-ranges={current_ip}/32 --project={self.project}"
            ]
            res = subprocess.run(wsl_cmd_update, capture_output=True)
            if res.returncode != 0:
                # Try to create if update fails
                wsl_cmd_create = [
                    "wsl", "-d", "kali-linux", "bash", "-c",
                    f"'{self.gcloud_path}' compute firewall-rules create {rule_name} --source-ranges={current_ip}/32 --project={self.project} --allow tcp:22 --description='Autonomous Sovereign Recovery'"
                ]
                res = subprocess.run(wsl_cmd_create, capture_output=True)
            
            return res.returncode == 0
        except Exception as e:
            print(f"[!] Firewall Recovery Failed: {e}")
            return False

if __name__ == "__main__":
    # Parameters to be filled dynamically or via environment
    # Defaults updated based on gcp_deploy_jarvis_backend.sh
    INSTANCE = os.environ.get("JARVIS_INSTANCE", "jarvis-central-core")
    PROJECT = os.environ.get("GCP_PROJECT", "SpartanAI-core-2026")
    ZONE = os.environ.get("GCP_ZONE", "us-central1-a")
    
    link = ApexLink(INSTANCE, PROJECT, ZONE)
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "--connect":
            link.connect_iap()
        elif action == "--harden":
            link.enable_serial_console()
            link.autonomous_firewall_recovery()
