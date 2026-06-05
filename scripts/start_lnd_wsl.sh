#!/bin/bash
# SpartanAI LND Launcher (WSL)
# MANDATE: Absolute Financial Sovereignty.

LND_BIN="/mnt/c/GitHub/SpartanAI_Core/tools/lnd/lnd"
LND_DIR="/mnt/c/GitHub/SpartanAI_Core/data/lnd"
CONF_FILE="$LND_DIR/lnd.conf"

echo "[*] Launching Sovereign LND Node in WSL..."
chmod +x "$LND_BIN"

# Start LND in background
nohup "$LND_BIN" --lnddir="$LND_DIR" --configfile="$CONF_FILE" > "$LND_DIR/lnd.log" 2>&1 &

echo "[+] LND Node process spawned. PID: $!"
echo "[*] Monitoring for initialization..."
sleep 5

if pgrep -f "$LND_BIN" > /dev/null; then
    echo "[+] LND Node is ACTIVE."
else
    echo "[!] LND Node failed to start. Check $LND_DIR/lnd.log"
fi
