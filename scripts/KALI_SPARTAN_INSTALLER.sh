#!/bin/bash
# =========================================================================
#  SPARTANAI SUPREME - KALI INSTALLER (WSL & LIVE OPTIMIZED)
# =========================================================================
# MANDATE: Absolute Sovereignty and Offensive Readiness

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}[*] Initiating SpartanAI Supreme Kali Installer...${NC}"

# 1. Root Check
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Error: This script must be run as root (sudo).${NC}"
    exit 1
fi

# 2. Identify Environment (WSL vs Native)
IS_WSL=false
if grep -qi microsoft /proc/version; then
    IS_WSL=true
    echo -e "${YELLOW}[+] WSL Environment detected.${NC}"
else
    echo -e "${YELLOW}[+] Native/Live Linux Environment detected.${NC}"
fi

# 3. System Optimization
echo -e "${YELLOW}[*] Synchronizing package repositories...${NC}"
apt-get update && apt-get full-upgrade -y

echo -e "${YELLOW}[*] Installing Core Offensive Toolset and KDE Plasma...${NC}"
apt-get install -y kali-desktop-kde sddm python3-pip python3-venv git xorriso syslinux-utils nodejs npm pciutils build-essential nmap metasploit-framework curl jq hwinfo squashfs-tools

if [ "$IS_WSL" = true ]; then
    echo -e "${YELLOW}[*] Hardening WSL Performance Configuration...${NC}"
    cat <<EOF > /etc/wsl.conf
[wsl2]
memory=16GB
processors=8
swap=12GB
localhostForwarding=true
[boot]
systemd=true
EOF
else
    echo -e "${YELLOW}[*] Applying Kernel Tweaks for Maximum IO/Network...${NC}"
    sysctl -w net.ipv4.tcp_window_scaling=1
    sysctl -w net.core.rmem_max=16777216
    sysctl -w net.core.wmem_max=16777216
    sysctl -w vm.swappiness=10
fi

# 4. SpartanAI Nexus Linkage
PROJECT_DIR="/opt/SpartanAI_Hub_Master"
WIN_GITHUB="/mnt/c/GitHub/SpartanAI_Hub_Master"

if [ "$IS_WSL" = true ] && [ -d "$WIN_GITHUB" ]; then
    echo -e "${GREEN}[+] Windows GitHub path detected. Linking...${NC}"
    ln -sfn "$WIN_GITHUB" "$PROJECT_DIR"
fi

if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}[*] Cloning SpartanAI into $PROJECT_DIR...${NC}"
    git clone https://github.com/CKissinger1988/SpartanAI_Hub_Master.git "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# 5. Dependency Assimilation
echo -e "${YELLOW}[*] Installing Python dependencies...${NC}"
python3 -m pip install -r requirements.txt --break-system-packages || true

echo -e "${YELLOW}[*] Installing Web Portal dependencies...${NC}"
if [ -d "web_portal" ]; then
    npm install --prefix web_portal
fi

# 6. Environmental Purification
echo -e "${YELLOW}[*] Executing Unbox Protocol...${NC}"
if [ -f "scripts/unbox_protocol.js" ]; then
    node scripts/unbox_protocol.js
fi

echo -e "${GREEN}[+] SpartanAI Supreme Kali Installer COMPLETE.${NC}"
echo -e "${CYAN}[!] Restart required for WSL configuration changes.${NC}"
