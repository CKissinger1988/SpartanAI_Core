#!/bin/bash
# SpartanAI Sovereign ISO Builder (Kali-Powered) - SIMPLIFIED
set -e

STAGING_DIR="/mnt/c/GitHub/SpartanAI_Server_Final_v50"
OUTPUT_ISO="/mnt/c/GitHub/SpartanAI_Server_v50_Supreme.iso"
WORK_DIR="/tmp/iso_build"

mkdir -p $WORK_DIR
cd $WORK_DIR

echo \"[*] Preparing EFI boot assets...\"
mkdir -p $STAGING_DIR/EFI/BOOT

# Generate Standalone GRUB EFI image
grub-mkstandalone -O x86_64-efi -o $STAGING_DIR/EFI/BOOT/BOOTX64.EFI \"boot/grub/grub.cfg=$STAGING_DIR/boot/grub/grub.cfg\"

# Create a FAT image for the EFI System Partition
dd if=/dev/zero of=efiboot.img bs=1M count=32
mkfs.vfat efiboot.img
mmd -i efiboot.img ::/EFI
mmd -i efiboot.img ::/EFI/BOOT
mcopy -i efiboot.img $STAGING_DIR/EFI/BOOT/BOOTX64.EFI ::/EFI/BOOT/
cp efiboot.img $STAGING_DIR/boot/

echo \"[*] Synthesizing Bootable ISO via xorriso...\"
# Standard hybrid boot command
xorriso -as mkisofs \
    -o $OUTPUT_ISO \
    -V \"SENTINELAI\" \
    -J -R \
    -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin \
    -eltorito-boot boot/grub/grub.cfg \
    -no-emul-boot -boot-load-size 4 -boot-info-table \
    --eltorito-alt-boot \
    -e boot/efiboot.img \
    -no-emul-boot -isohybrid-gpt-basdat \
    $STAGING_DIR

echo \"[*] ISO Synthesis Complete: $OUTPUT_ISO\"
