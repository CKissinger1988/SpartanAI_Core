#!/bin/bash
# NEXUS // AI - Kali ISO Integration Script (v2.0 - UEFI & Preseed Fix)
set -e

# --- Configuration ---
BASE_ISO="kali-linux-2026.1-installer-netinst-amd64.iso"
MOD_ISO_NAME="NEXUS_AI_KALI_AUTOMATED_UEFI.iso"
PROJECT_DIR="/mnt/c/Users/ckiss" # Mount point for the project directory
WORKSPACE="workspace"
ISO_MOUNT_POINT="iso_orig"
ISO_BUILD_DIR="iso_build"

echo "--- NEXUS // AI: KALI ISO AUTOMATED INTEGRATION (v2.0) ---"

# --- 1. Prepare Workspace ---
echo "[+] Preparing workspace..."
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"
mkdir -p "$ISO_MOUNT_POINT" "$ISO_BUILD_DIR"

# --- 2. Mount and Extract Original ISO ---
echo "[+] Mounting and extracting original Kali ISO..."
# Requires sudo permissions
sudo mount -o loop "../$BASE_ISO" "$ISO_MOUNT_POINT"
# Copy all files to have write permissions
rsync -av "$ISO_MOUNT_POINT/" "$ISO_BUILD_DIR/"
sudo umount "$ISO_MOUNT_POINT"
echo "[+] ISO extracted. Working in '$ISO_BUILD_DIR'."

# --- 3. Integrate Project Files & Preseed ---
echo "[+] Integrating Nexus project files..."
mkdir -p "$ISO_BUILD_DIR/opt/nexus-ai"
ITEMS=(
    "app" "backend" "src" "JarvisAI_Stable" "SentinelAI"
    "physpanel" "scripts" "package.json" "Dockerfile"
    "webpack.config.js" "jest.config.js" "README.md"
)
for item in "${ITEMS[@]}"; do
    if [ -e "$PROJECT_DIR/$item" ]; then
        cp -r "$PROJECT_DIR/$item" "$ISO_BUILD_DIR/opt/nexus-ai/"
    fi
done

echo "[+] Integrating preseed configuration..."
cp "$PROJECT_DIR/preseed.cfg" "$ISO_BUILD_DIR/preseed.cfg"
chmod 644 "$ISO_BUILD_DIR/preseed.cfg"

# --- 4. Modify Bootloader for Automation (UEFI & BIOS) ---
echo "[+] Patching bootloader configurations for unattended install..."
# This is the critical step for automation
PRESEED_PARAMS="auto=true priority=critical preseed/file=/cdrom/preseed.cfg"

# For BIOS boot
# Find the default menu entry and append the preseed params
# Using a temp file for sed compatibility
sed "s|^\s*append.*|& ${PRESEED_PARAMS}|g" "$ISO_BUILD_DIR/isolinux/txt.cfg" > "$ISO_BUILD_DIR/isolinux/txt.cfg.tmp"
mv -f "$ISO_BUILD_DIR/isolinux/txt.cfg.tmp" "$ISO_BUILD_DIR/isolinux/txt.cfg"

# For UEFI boot
sed -i "s|^\s*linux\s*/install/vmlinuz.*|& ${PRESEED_PARAMS}|g" "$ISO_BUILD_DIR/boot/grub/grub.cfg"

echo "[+] Bootloaders patched."

# --- 5. Rebuild ISO with UEFI & BIOS Hybrid Boot ---
echo "[+] Installing boot utilities..."
sudo apt-get update && sudo apt-get install -y syslinux-utils

echo "[+] Rebuilding ISO with hybrid boot support..."
cd "$ISO_BUILD_DIR"

xorriso -as mkisofs -r -V "NEXUS_AI_KALI" -o "../../$MOD_ISO_NAME" -J -joliet-long -cache-inodes -isohybrid-mbr /usr/lib/syslinux/isohdpfx.bin -b isolinux/isolinux.bin -c isolinux/boot.cat -boot-load-size 4 -boot-info-table -no-emul-boot -eltorito-alt-boot -e boot/grub/efi.img -no-emul-boot -isohybrid-gpt-basdat .

cd ..
echo "--- INTEGRATION COMPLETE ---"
echo "Production ISO: ../$MOD_ISO_NAME"
echo "This ISO is now UEFI & BIOS compatible and fully automated."
