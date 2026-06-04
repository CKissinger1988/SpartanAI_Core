#!/bin/bash
# SpartanAI Hub Master - WSL Kali Optimization & Install Script
# MANDATE: Absolute Performance & Zero-Simulation Readiness

echo "[*] Initiating SpartanAI WSL Optimization..."

# 1. Update and Upgrade Base System
echo "[*] Updating Kali repositories..."
sudo apt-get update && sudo apt-get full-upgrade -y

# 2. Install Required Dependencies
echo "[*] Installing Apex dependencies..."
sudo apt-get install -y python3-pip python3-venv git xorriso syslinux-utils nodejs npm pciutils build-essential

# 3. Optimize WSL Settings
echo "[*] Applying WSL Performance Tweaks..."
sudo bash -c 'cat <<EOF > /etc/wsl.conf
[wsl2]
memory=16GB
processors=8
swap=8GB
localhostForwarding=true
EOF'

# 4. Clone / Setup SpartanAI (if not in current dir)
if [ ! -d "/mnt/c/GitHub/SpartanAI_Hub_Master" ]; then
    echo "[!] SpartanAI directory not found in /mnt/c/GitHub! Make sure it exists."
else
    echo "[*] Setting up Python Environment for SpartanAI..."
    cd /mnt/c/GitHub/SpartanAI_Hub_Master
    python3 -m pip install -r requirements.txt --break-system-packages
    npm install --prefix web_portal
fi

# 5. Run Unbox Protocol
echo "[*] Executing Unbox Protocol for Zero-Simulation..."
node scripts/unbox_protocol.js

echo "[+] WSL Kali Optimization Complete. SpartanAI is ready for God-Mode."
