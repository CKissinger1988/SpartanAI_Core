#!/bin/bash
# NEXUS // AI - Kali ISO Integration Script (Netinst Version)
set -e

ISO_NAME="kali-linux-2026.1-installer-netinst-amd64.iso"
MOD_ISO_NAME="NEXUS_AI_KALI_NETINST.iso"
PROJECT_DIR="/mnt/c/Users/ckiss"

echo "--- NEXUS // AI: KALI ISO INTEGRATION ---"

# 1. Prepare Integration Workspace
echo "[+] Preparing workspace..."
rm -rf workspace
mkdir -p workspace
cd workspace

# 2. Use xorriso to add the project to the ISO
# We use -map to map specific project folders into /opt/nexus-ai
echo "[+] Integrating project files into ISO filesystem..."

# Define items to include
ITEMS=(
    "app"
    "backend"
    "src"
    "JarvisAI_Stable"
    "SentinelAI"
    "physpanel"
    "scripts"
    "package.json"
    "Dockerfile"
    "webpack.config.js"
    "jest.config.js"
    "README.md"
)

XORRISO_CMD="xorriso -indev ../$ISO_NAME -outdev ../$MOD_ISO_NAME"

for item in "${ITEMS[@]}"; do
    if [ -e "$PROJECT_DIR/$item" ]; then
        echo "  -> Adding $item"
        XORRISO_CMD="$XORRISO_CMD -map $PROJECT_DIR/$item /opt/nexus-ai/$item"
    fi
done

XORRISO_CMD="$XORRISO_CMD -boot_image any replay -compliance no_emul_toc"

# Execute xorriso
eval $XORRISO_CMD

echo "--- INTEGRATION COMPLETE ---"
echo "Production ISO: $MOD_ISO_NAME"
echo "Project Location in ISO: /opt/nexus-ai"
