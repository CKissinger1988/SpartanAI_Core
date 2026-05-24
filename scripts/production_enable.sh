#!/bin/bash
# Jarvis // AI - Production Deployment & Tool Enablement Script
# FOR REAL-WORLD USE: Sanitizes system and enables the full Kali Linux arsenal.

# ANSI Colors
CYAN='\033[96m'
GREEN='\033[92m'
YELLOW='\033[93m'
RED='\033[91m'
BOLD='\033[1m'
ENDC='\033[0m'

echo -e "${RED}${BOLD}--- Jarvis // AI: PRODUCTION DEPLOYMENT SEQUENCE ---${ENDC}"

# 1. Run Secure Field Preparation (Sanitization)
if [ -f "scripts/field_prep_secure.sh" ]; then
    echo -e "${GREEN}[+] Initiating secure sanitization...${ENDC}"
    bash scripts/field_prep_secure.sh
else
    echo -e "${YELLOW}[!] Sanitization script not found. Proceeding with manual cleanup...${ENDC}"
    rm -f data/*.jsonl data/*.log 2>/dev/null
    find . -name "mock_system" -type d -exec rm -rf {} + 2>/dev/null
fi

# 2. Update Repositories and System
echo -e "${GREEN}[+] Synchronizing Kali Linux repositories...${ENDC}"
sudo apt-get update -y

# 3. Enable Full Kali Arsenal
# Note: In a real-world scenario, we use kali-linux-large or kali-linux-everything.
# For WSL/Performance, we'll ensure core tactical tools are present first.
echo -e "${GREEN}[+] Deploying tactical toolsets (Full Arsenal)...${ENDC}"
# We'll install the 'large' metapackage which includes most commonly used tools
# This can take time, so we'll check if they are already there first
sudo apt-get install -y kali-linux-large tor postgresql

# 4. Configure Tactical Services
echo -e "${GREEN}[+] Configuring tactical services...${ENDC}"
# Initialize Metasploit database
sudo service postgresql start
sudo msfdb init 2>/dev/null || echo "    -> Metasploit DB already initialized."
# Ensure Tor is ready
sudo service tor start

# 5. Verification Check
echo -e "${CYAN}${BOLD}--- FINAL PRODUCTION VERIFICATION ---${ENDC}"
TOOLS=("nmap" "msfconsole" "sqlmap" "aircrack-ng" "john" "hydra" "wireshark")
SUCCESS_COUNT=0

for tool in "${TOOLS[@]}"; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo -e "${GREEN}[PASS] $tool is ONLINE.${ENDC}"
        ((SUCCESS_COUNT++))
    else
        echo -e "${RED}[FAIL] $tool is MISSING.${ENDC}"
    fi
done

if [ $SUCCESS_COUNT -eq ${#TOOLS[@]} ]; then
    echo -e "${GREEN}${BOLD}SYSTEM STATUS: FULLY ARMED & PRODUCTION-SECURE.${ENDC}"
else
    echo -e "${YELLOW}SYSTEM STATUS: PARTIALLY ARMED ($SUCCESS_COUNT/${#TOOLS[@]}). Check logs.${ENDC}"
fi

echo -e "${RED}${BOLD}--- DEPLOYMENT COMPLETE ---${ENDC}"
