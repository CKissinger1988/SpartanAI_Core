# scripts/kali_bootstrap.sh
# Final-Stage Bootstrap for SpartanAI Terminal - Kali WSL
# MANDATE: Absolute Autonomy & Offensive Readiness

echo -e "\x1b[35m\x1b[1m[*] Initiating SpartanAI Kali Bootstrap...\x1b[0m"

# 1. Update and Upgrade
echo "[*] Synchronizing package repositories..."
sudo apt-get update && sudo apt-get full-upgrade -y

# 2. Install Core Offensive Toolset
echo "[*] Installing SpartanAI Core Dependencies..."
sudo apt-get install -y python3-pip python3-venv git xorriso syslinux-utils nodejs npm pciutils build-essential nmap metasploit-framework curl jq

# 3. Optimize WSL Settings
echo "[*] Hardening WSL Performance Configuration..."
sudo bash -c 'cat <<EOF > /etc/wsl.conf
[wsl2]
memory=16GB
processors=8
swap=12GB
localhostForwarding=true
[boot]
systemd=true
EOF'

# 4. Project Linkage (Assume Windows path is /mnt/c/GitHub/SpartanAI_Terminal)
PROJECT_DIR="/mnt/c/GitHub/SpartanAI_Terminal"

if [ -d "$PROJECT_DIR" ]; then
    echo "[+] Project directory detected. Mapping offensive assets..."
    cd "$PROJECT_DIR"
    
    # Install Python Dependencies (Sovereign Mode)
    if [ -f "requirements.txt" ]; then
        python3 -m pip install -r requirements.txt --break-system-packages
    fi
    
    # Install Root Node Dependencies
    npm install
    
    # Execute Master Purity Script
    echo "[*] Enforcing Zero-Simulation Policy via Master Script..."
    node scripts/universal_debug_purity.js --purity
else
    echo -e "\x1b[31m[!] Project directory not found at $PROJECT_DIR! Skipping project-specific setup.\x1b[0m"
fi

echo -e "\x1b[32m\x1b[1m[+] SpartanAI Kali Bootstrap COMPLETE. Environment is PURIFIED.\x1b[0m"
