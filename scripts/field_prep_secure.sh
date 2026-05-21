#!/bin/bash
# NEXUS // AI - Secure Field Preparation & Sanitization Script
# FOR REAL-WORLD USE: Purges all traces of simulation, sandboxes, and development artifacts.

# ANSI Colors
CYAN='\033[96m'
GREEN='\033[92m'
YELLOW='\033[93m'
RED='\033[91m'
BOLD='\033[1m'
ENDC='\033[0m'

echo -e "${RED}${BOLD}--- NEXUS // AI: SECURE FIELD PREPARATION ---${ENDC}"
echo -e "${YELLOW}[!] WARNING: This will permanently destroy all simulation data and test profiles.${ENDC}"

# Function to securely wipe if shred is available, otherwise rm
secure_purge() {
    if command -v shred >/dev/null 2>&1; then
        shred -u -z -n 3 "$1" 2>/dev/null || rm -rf "$1"
    else
        rm -rf "$1"
    fi
}

# 1. Purge Simulation Logs & Behavioral Data
echo -e "${GREEN}[+] Sanitizing behavioral and telemetry logs...${ENDC}"
LOGS=(
    "data/behavioral_observations.jsonl"
    "data/unauthorized_access.log"
    "nexus_intelligence.db-journal"
)
for log in "${LOGS[@]}"; do
    if [ -f "$log" ]; then
        secure_purge "$log"
        echo "    -> Log sanitized: $log"
    fi
done

# 2. Purge Mock Systems & Sandboxes
echo -e "${GREEN}[+] Purging simulation sandboxes...${ENDC}"
MOCK_DIRS=$(find . -name "mock_system" -type d)
for dir in $MOCK_DIRS; do
    echo "    -> Shredding sandbox: $dir"
    rm -rf "$dir" # rm -rf is safer for directories; shred for individual files inside if needed
done

# 3. Purge Test Profiles & Vector Data
echo -e "${GREEN}[+] Wiping non-Creator user profiles and vector metadata...${ENDC}"
# Keep only the Creator profile if it exists, or wipe all for fresh start
if [ -d "data/profiles" ]; then
    find data/profiles -type f ! -name "Creator.json" -delete
    echo "    -> Test profiles purged."
fi

if [ -d "vector_db" ]; then
    rm -rf vector_db/*
    echo "    -> Vector database sanitized."
fi

# 4. Purge Development & Build Artifacts
echo -e "${GREEN}[+] Removing build workspaces and ISO artifacts...${ENDC}"
rm -rf workspace/
rm -f *.iso
rm -f *.zip
echo "    -> Build artifacts removed."

# 5. Clear Environment & History
echo -e "${GREEN}[+] Sanitizing terminal history and caches...${ENDC}"
secure_purge ~/.bash_history
secure_purge ~/.zsh_history
history -c 2>/dev/null

# Clear Python and Node caches
find . -type d -name "__pycache__" -not -path "*/venv/*" -not -path "*/node_modules/*" -exec rm -rf {} + 2>/dev/null
rm -rf ~/.npm/_cacache
echo "    -> Environment sanitized."

# 6. Remove Security Risks
echo -e "${GREEN}[+] Removing plaintext credential files...${ENDC}"
secure_purge "INITIAL_CREDENTIALS.txt"
secure_purge "2FA_SETUP.json" # If not needed for prod
echo "    -> Credential artifacts removed."

echo -e "${RED}${BOLD}--- FIELD PREP COMPLETE. SYSTEM STATE: PRODUCTION-SECURE ---${ENDC}"
