#!/bin/bash
set -e

echo "========================================================="
echo "        SPARTANAI GCP OS - DOCKER CONTAINMENT            "
echo "========================================================="

echo "[*] Initializing Python Virtual Environment..."
source /opt/venv/bin/activate

echo "[*] Synchronizing Neural DB & Configuration..."
python3 scripts/status_check.py

echo "[*] Launching Financial Cortex (LND)..."
nohup /opt/spartanai/tools/lnd/lnd --lnddir=/opt/spartanai/data/lnd --configfile=/opt/spartanai/data/lnd/lnd.conf > /opt/spartanai/data/lnd/lnd.log 2>&1 &

echo "[*] Waiting for LND Daemon to initialize..."
sleep 5

echo "[*] Unlocking LND Wallet..."
python3 scripts/unlock_lnd.py || echo "[!] Wallet unlock failed. Remote initialization may be required."

echo "[*] Engaging MCP LM-Studio Bridge..."
# Assuming we run this in the background if it exists
if [ -f "backend/core/mcp_lms_bridge.py" ]; then
    nohup python3 backend/core/mcp_lms_bridge.py > bridge.log 2>&1 &
fi

echo "========================================================="
echo "        CORTEX ACTIVE. YIELDING TO TAIL LOG.             "
echo "========================================================="

# Keep the container running by tailing the LND logs
tail -f /opt/spartanai/data/lnd/lnd.log
