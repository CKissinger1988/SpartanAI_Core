#!/bin/bash
# NEXUS // AI - Kali ISO Integration Script
# This script downloads the latest Kali Rolling Live ISO and 
# integrates the Sentinel Hub project for instant deployment.

set -e

ISO_URL="https://cdimage.kali.org/kali-2026.1/kali-linux-2026.1-live-amd64.iso"
ISO_NAME="kali-linux-2026.1-live-amd64.iso"
MOD_ISO_NAME="NEXUS_AI_KALI_v3.1.0.iso"
PROJECT_DIR="/mnt/c/Users/ckiss"

echo "--- NEXUS // AI: KALI ISO INTEGRATION ---"

# 1. Download the ISO (if not present)
if [ ! -f "$ISO_NAME" ]; then
    echo "[+] Downloading latest Kali Rolling ISO..."
    curl -L "$ISO_URL" -o "$ISO_NAME"
else
    echo "[*] Base ISO found locally."
fi

# 2. Prepare Integration Workspace
echo "[+] Preparing workspace..."
mkdir -p workspace
cd workspace

# 3. Use xorriso to add the project to the ISO
# We add the project to /opt/nexus-ai
echo "[+] Integrating project files into ISO filesystem..."
xorriso -indev "../$ISO_NAME" \
        -outdev "../$MOD_ISO_NAME" \
        -add "$PROJECT_DIR"=/opt/nexus-ai \
        -boot_image any replay \
        -compliance no_emul_toc

echo "--- INTEGRATION COMPLETE ---"
echo "Production ISO: $MOD_ISO_NAME"
echo "Project Location in ISO: /opt/nexus-ai"
