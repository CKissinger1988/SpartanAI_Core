#!/bin/bash
# SpartanAI Hub Master - Kali Live USB Optimization & Persistence Setup
# MANDATE: Hardware-Level Ascension and Ephemeral Supremacy

echo "[*] Initiating SpartanAI Kali Live Setup..."

# 1. Mount Persistence Partition (if applicable)
echo "[*] Ensuring persistence..."
if ! grep -q "persistence" /proc/cmdline; then
    echo "[!] Warning: Not booted in persistence mode. Changes will be lost on reboot."
fi

# 2. System Update & Optimization
echo "[*] Updating live environment packages..."
sudo apt-get update
sudo apt-get install -y python3-pip git nodejs npm hwinfo xorriso

# 3. Kernel Parameter Tweaks
echo "[*] Applying Kernel Tweaks for Maximum IO/Network..."
sudo sysctl -w net.ipv4.tcp_window_scaling=1
sudo sysctl -w net.core.rmem_max=16777216
sudo sysctl -w net.core.wmem_max=16777216
sudo sysctl -w vm.swappiness=10

# 4. Install SpartanAI
TARGET_DIR="/opt/SpartanAI_Hub_Master"
if [ ! -d "$TARGET_DIR" ]; then
    echo "[*] Cloning SpartanAI into $TARGET_DIR..."
    sudo git clone https://github.com/ToxicSavage304/SpartanAI_Hub_Master.git $TARGET_DIR
fi

echo "[*] Setting up dependencies..."
cd $TARGET_DIR
sudo python3 -m pip install -r requirements.txt --break-system-packages
sudo npm install --prefix web_portal

# 5. Purify Environment
echo "[*] Executing Unbox Protocol..."
sudo node scripts/unbox_protocol.js

echo "[+] Kali Live Environment Optimized. SpartanAI Nexus ONLINE."
