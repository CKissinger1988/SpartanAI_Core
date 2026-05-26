#!/bin/bash
# =========================================================================
#  SENTINEL-OS // LIVE UPLINK SYNC
# =========================================================================
# Monitors the local repository and pulls updates to the WSL environment.

REPO_PATH="/mnt/c/GitHub/SpartanAI_Hub_Master"
SYNC_INTERVAL=30 # seconds

echo "[+] Uplink active. Monitoring $REPO_PATH..."

while true; do
    cd "$REPO_PATH"
    if [ -d ".git" ]; then
        # Perform git pull and output to log
        git pull origin main --quiet 2>/dev/null
        
        # Check if changes were pulled
        if [ $? -eq 0 ]; then
            # Optional: Add hook for hot-reloading Jarvis core if needed
            # e.g., pkill -f jarvis.py && nohup python3 backend/core/jarvis.py &
            : 
        fi
    fi
    sleep $SYNC_INTERVAL
done
