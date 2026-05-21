#!/bin/bash
# NEXUS // AI - Autonomous Simulation Purge Script
# This script removes mock environments, simulation logs, and build artifacts from Kali Linux.

# ANSI Colors
CYAN='\033[96m'
GREEN='\033[92m'
RED='\033[91m'
BOLD='\033[1m'
ENDC='\033[0m'

echo -e "${CYAN}${BOLD}--- NEXUS // AI: TACTICAL SIMULATION PURGE ---${ENDC}"

# 1. Purge Behavioral Observation Logs
OBS_LOG="data/behavioral_observations.jsonl"
if [ -f "$OBS_LOG" ]; then
    echo -e "${GREEN}[+] Purging behavioral observation logs...${ENDC}"
    rm "$OBS_LOG"
    echo "    -> $OBS_LOG removed."
else
    echo -e "${CYAN}[i] No behavioral logs found.${ENDC}"
fi

# 2. Purge Mock Installation Systems
echo -e "${GREEN}[+] Scanning for mock installation environments...${ENDC}"
MOCK_DIRS=$(find . -name "mock_system" -type d)
if [ -n "$MOCK_DIRS" ]; then
    for dir in $MOCK_DIRS; do
        echo "    -> Removing $dir"
        rm -rf "$dir"
    done
    echo -e "${GREEN}    -> All mock systems purged.${ENDC}"
else
    echo "    -> No mock systems detected."
fi

# 3. Purge ISO Build Workspaces
WORKSPACE_DIR="workspace"
if [ -d "$WORKSPACE_DIR" ]; then
    echo -e "${GREEN}[+] Purging ISO build workspace...${ENDC}"
    rm -rf "$WORKSPACE_DIR"
    echo "    -> $WORKSPACE_DIR removed."
else
    echo -e "${CYAN}[i] No build workspace detected.${ENDC}"
fi

# 4. Cleanup Python/Testing Caches
echo -e "${GREEN}[+] Cleaning temporary caches and test artifacts (excluding venv/node_modules)...${ENDC}"
find . -type d -name "__pycache__" -not -path "*/venv/*" -not -path "*/node_modules/*" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".pytest_cache" -not -path "*/venv/*" -not -path "*/node_modules/*" -exec rm -rf {} + 2>/dev/null
echo "    -> Internal caches cleared."

# 5. Remove Simulation Scripts Results (if any)
# Specifically target files created by scripts/simulate_install.sh in specific locations
# (Covered by mock_system check, but being explicit)

echo -e "${CYAN}${BOLD}--- PURGE COMPLETE. SYSTEM POSTURE: SECURE ---${ENDC}"
