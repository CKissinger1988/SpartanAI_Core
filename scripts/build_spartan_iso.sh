#!/bin/bash
# =========================================================================
#  SPARTANAI SUPREME - ISO FOUNDRY (C-DRIVE STAGING)
# =========================================================================
set -e

ISO_NAME="SpartanAI_Server_Install.iso"
PROJECT_ROOT="/mnt/c/GitHub/SpartanAI_Hub_Master"
STAGING="/mnt/c/GitHub/spartan_iso_staging"
RELEASES_DIR="$PROJECT_ROOT/releases"
BURN_TARGET="/mnt/d"

echo "[*] Initializing Staging Area at $STAGING..."
rm -rf "$STAGING"
mkdir -p "$STAGING/boot/grub"

echo "[*] Copying Boot Assets..."
cp "$PROJECT_ROOT/boot/vmlinuz" "$STAGING/boot/"
cp "$PROJECT_ROOT/boot/initrd.img" "$STAGING/boot/"
cp "$PROJECT_ROOT/boot/grub/grub.cfg" "$STAGING/boot/grub/"

echo "[*] Ingesting Project Shards (Surgical Copy)..."
mkdir -p "$STAGING/spartan"
cp -r "$PROJECT_ROOT/backend" "$STAGING/spartan/"
cp -r "$PROJECT_ROOT/Protocols" "$STAGING/spartan/"
cp -r "$PROJECT_ROOT/scripts" "$STAGING/spartan/"
cp -r "$PROJECT_ROOT/tools" "$STAGING/spartan/"
mkdir -p "$STAGING/spartan/web_portal"
cp -r "$PROJECT_ROOT/web_portal/src" "$STAGING/spartan/web_portal/"
cp "$PROJECT_ROOT/web_portal/package.json" "$STAGING/spartan/web_portal/"
cp "$PROJECT_ROOT/requirements.txt" "$STAGING/spartan/"
cp "$PROJECT_ROOT/"*.md "$STAGING/spartan/"
cp "$PROJECT_ROOT/"*.txt "$STAGING/spartan/"
cp "$PROJECT_ROOT/"*.py "$STAGING/spartan/"
cp "$PROJECT_ROOT/"*.sh "$STAGING/spartan/"

echo "[*] Compiling Supreme ISO..."
xorriso -as mkisofs \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid "SPARTAN_AI" \
    -eltorito-boot boot/grub/grub.cfg \
    -no-emul-boot -boot-load-size 4 -boot-info-table \
    -output "$RELEASES_DIR/$ISO_NAME" \
    "$STAGING"

echo "[+] ISO Build Complete: $RELEASES_DIR/$ISO_NAME"

if [ -d "$BURN_TARGET" ]; then
    echo "[*] Burning (Copying) to $BURN_TARGET..."
    cp "$RELEASES_DIR/$ISO_NAME" "$BURN_TARGET/"
    echo "[+] Burn Successful."
else
    echo "[!] D:/ drive not detected at $BURN_TARGET. Skipping burn."
fi
