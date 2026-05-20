#!/bin/bash
# build_rhel_ai_iso.sh - Automated Custom OS Builder
# Compiles the JarvisAI Supreme Core into a bootable Red Hat Enterprise Linux AI OS image.
# Requires 'mkksiso' (part of the 'lorax' package) on a Fedora/RHEL system.

set -e

echo "--- Initializing JarvisAI RHEL AI OS Compilation ---"

# 1. Dependency Check
if ! command -v mkksiso &> /dev/null; then
    echo "ERROR: 'mkksiso' tool is missing."
    echo "Please install the 'lorax' package (e.g., sudo dnf install lorax) on your build machine."
    exit 1
fi

BASE_ISO="rhel-ai-9-x86_64-boot.iso"
OUTPUT_ISO="JarvisAI_Supreme_OS_v1.3.0.iso"
KICKSTART="jarvis_rhel_ai.ks"

# 2. Base OS Verification
if [ ! -f "$BASE_ISO" ]; then
    echo "ERROR: Red Hat Enterprise Linux AI Base ISO ('$BASE_ISO') not found."
    echo "Download the official RHEL AI Boot ISO and place it in this directory before building."
    exit 1
fi

if [ ! -f "$KICKSTART" ]; then
    echo "ERROR: Kickstart configuration ('$KICKSTART') not found."
    exit 1
fi

# 3. Compile OS Image
echo "Injecting Supreme Core kickstart configuration into RHEL AI Base Image..."
echo "This will bundle the Encrypted Vaults, Pi Synergy, and Ghost Integrity directly into the OS..."

# mkksiso embeds the kickstart and modifies the boot menus to run it automatically
sudo mkksiso --ks "$KICKSTART" "$BASE_ISO" "$OUTPUT_ISO"

echo "--- Compilation SUCCESS ---"
echo "Custom OS Image Generated: $OUTPUT_ISO"
echo "Deployment: Boot this ISO on bare metal or any hypervisor. JarvisAI will automatically install, configure the multi-container architecture, and run flawlessly out-of-the-box."
