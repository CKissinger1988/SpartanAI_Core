#!/bin/bash
# =========================================================================
#  SPARTANAI APEX - UNIVERSAL VM OPTIMIZED ISO GENERATOR
# =========================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}=========================================================${NC}"
echo -e "${CYAN}      SPARTANAI APEX - UNIVERSAL VM ISO FOUNDRY${NC}"
echo -e "${CYAN}=========================================================${NC}"

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Error: This script must be run as root (sudo).${NC}"
    exit 1
fi

# 1. Workspace Initialization
BUILD_DIR="/opt/spartanai_vm_optimized_build"
echo -e "${YELLOW}[*] Initializing VM-Optimized workspace: ${BUILD_DIR}${NC}"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

# 2. Tool Verification
echo -e "${YELLOW}[*] Verifying build tools...${NC}"
apt-get update -qq
apt-get install -y -qq live-build xorriso squashfs-tools curl git isolinux syslinux-common qemu-utils

# 3. Configure live-build
echo -e "${YELLOW}[*] Configuring live-build...${NC}"
lb config \
    --binary-images iso \
    --distribution noble \
    --archive-areas "main restricted universe multiverse" \
    --apt-recommends false \
    --linux-flavours generic \
    --parent-mirror-bootstrap "http://archive.ubuntu.com/ubuntu/" \
    --mirror-bootstrap "http://archive.ubuntu.com/ubuntu/" \
    --parent-mirror-chroot-security "http://security.ubuntu.com/ubuntu/" \
    --mirror-chroot-security "http://security.ubuntu.com/ubuntu/" \
    --parent-mirror-binary-security "http://security.ubuntu.com/ubuntu/" \
    --mirror-binary-security "http://security.ubuntu.com/ubuntu/"

# 4. Package Configuration
echo -e "${YELLOW}[*] Staging package lists...${NC}"
mkdir -p config/package-lists
cat <<EOF > config/package-lists/vm-optimized.list.chroot
qemu-guest-agent
open-vm-tools
virtualbox-guest-utils
cloud-init
virtio-drivers
curl
git
python3
python3-pip
EOF

# 5. Core Overlay
echo -e "${YELLOW}[*] Overlaying SpartanAI Core via tar pipeline...${NC}"
OVERLAY_DIR="${BUILD_DIR}/config/includes.chroot/opt/spartanai"
mkdir -p "$OVERLAY_DIR"

SOURCE="/mnt/c/GitHub/SpartanAI_Hub_Master"
cd "$SOURCE"

# Define items to include
INCLUDE_ITEMS="backend boot data encrypted_payload Protocols scripts tools web_portal/src web_portal/package.json *.md *.txt *.py *.sh *.jpg"

# Use tar to copy surgically and robustly
tar cf - $INCLUDE_ITEMS --exclude=".git" --exclude=".vs" --exclude="node_modules" --exclude="temp_*" --exclude="*.iso" --exclude="*.qcow2" --exclude="*.vmdk" --exclude="releases" | (cd "$OVERLAY_DIR" && tar xf -)

cd "$BUILD_DIR"

# 6. Build
echo -e "${YELLOW}[*] Compiling ISO...${NC}"
if lb build; then
    echo -e "${GREEN}[+] lb build successful.${NC}"
else
    echo -e "${RED}[!] Build failed. Attempting manual ISO salvage from current state...${NC}"
    if [ -d "binary" ]; then
        xorriso -as mkisofs -o "spartanai_apex_vm_optimized.iso" -R -J -V 'SPARTANAI_VM' binary/
    else
        echo -e "${RED}[!] Critical: 'binary' directory not found. Salvage impossible.${NC}"
        exit 1
    fi
fi

# 7. Deployment
FINAL_ISO="spartanai_apex_vm_optimized.iso"
# Check if lb build produced an image (usually live-image-amd64.iso)
if [ -f "live-image-amd64.iso" ]; then
    mv "live-image-amd64.iso" "$FINAL_ISO"
fi

if [ -f "$FINAL_ISO" ]; then
    cp "$FINAL_ISO" "/mnt/c/GitHub/SpartanAI_Hub_Master/releases/"
    echo -e "${GREEN}[+] ISO deployed to releases folder.${NC}"
    
    # Burn to D: (Try to mount if needed, but assuming D: is available in WSL)
    if [ -d "/mnt/d" ]; then
        cp "$FINAL_ISO" "/mnt/d/"
        echo -e "${GREEN}[+] ISO burned to D:/ complete.${NC}"
    else
        echo -e "${RED}[!] D:/ not found in /mnt/d. Skipping burn.${NC}"
    fi
else
    echo -e "${RED}[!] ISO file not found after build.${NC}"
fi

echo -e "${CYAN}=========================================================${NC}"
echo -e "${GREEN}      VM-OPTIMIZED FOUNDRY COMPLETE${NC}"
echo -e "${CYAN}=========================================================${NC}"
