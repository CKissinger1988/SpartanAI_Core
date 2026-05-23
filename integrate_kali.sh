#!/bin/bash
# NEXUS // AI - Kali ISO Integration Script
set -e

ISO_NAME="kali-linux-2026.1-live-amd64.iso"
MOD_ISO_NAME="NEXUS_AI_KALI_v3.1.0.iso"
PROJECT_DIR="/home/pentester/nexusai"

echo "--- NEXUS // AI: KALI ISO INTEGRATION ---"

# 2. Prepare Integration Workspace
echo "[+] Preparing workspace..."
mkdir -p workspace

# 3. Use xorriso to add the project to the ISO
echo "[+] Integrating project files into ISO filesystem..."
xorriso -indev "$ISO_NAME" 
        -outdev "workspace/$MOD_ISO_NAME" 
        -add "$PROJECT_DIR"=/opt/nexus-ai 
        -boot_image any replay 
        -compliance no_emul_toc

echo "--- INTEGRATION COMPLETE ---"
echo "Production ISO: workspace/$MOD_ISO_NAME"
EOF
