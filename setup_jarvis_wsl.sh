#!/bin/bash
# NEXUS // AI - WSL Setup Script
# Run this inside your Kali WSL instance to prepare the environment.

set -e

echo "[+] Setting up NEXUS // AI environment in Kali WSL..."

# 1. Update system and install dependencies
echo "[+] Updating system..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nodejs npm

# 2. Setup Python environment
echo "[+] Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Setup Node environment
echo "[+] Installing Node dependencies..."
npm install

echo "--- SETUP COMPLETE ---"
echo "You can now run 'source venv/bin/activate' to start the environment."
