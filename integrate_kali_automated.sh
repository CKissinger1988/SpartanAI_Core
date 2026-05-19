#!/bin/bash
# NEXUS // AI - Kali ISO Integration Script (Automated Version)
set -e

ISO_NAME="kali-linux-2026.1-installer-netinst-amd64.iso"
MOD_ISO_NAME="NEXUS_AI_KALI_AUTOMATED.iso"
PROJECT_DIR="/mnt/c/Users/ckiss"

echo "--- NEXUS // AI: KALI ISO AUTOMATED INTEGRATION ---"

# 1. Prepare Integration Workspace
echo "[+] Preparing workspace..."
rm -rf workspace
mkdir -p workspace
cd workspace

# 2. Extract and modify boot configuration for automation
# We'll use xorriso to add the preseed.cfg and modify the boot menu
echo "[+] Integrating project files and automation..."

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

# Start building the xorriso command
# We use -map to place preseed.cfg at the root of the ISO
XORRISO_CMD="xorriso -indev ../$ISO_NAME -outdev ../$MOD_ISO_NAME"
XORRISO_CMD="$XORRISO_CMD -map $PROJECT_DIR/preseed.cfg /preseed.cfg"

# Add project files to /opt/nexus-ai
for item in "${ITEMS[@]}"; do
    if [ -e "$PROJECT_DIR/$item" ]; then
        XORRISO_CMD="$XORRISO_CMD -map $PROJECT_DIR/$item /opt/nexus-ai/$item"
    fi
done

# Boot image options (keeping original hybrid boot)
XORRISO_CMD="$XORRISO_CMD -boot_image any replay -compliance no_emul_toc"

# Execute xorriso
eval $XORRISO_CMD

echo "--- INTEGRATION COMPLETE ---"
echo "Production ISO: $MOD_ISO_NAME"
echo "Project Location in ISO: /opt/nexus-ai"
echo "Automation: preseed.cfg integrated."
