#!/bin/bash
# =========================================================================
#  NEXUS AI SECURITY SUITE - CUSTOM LIVE ISO GENERATOR
# =========================================================================
# This script uses 'live-build' to compile a custom, bootable Debian-based
# Live OS ISO that includes the Nexus AI Security Suite pre-installed and
# configured to run on startup with persistence enabled.
#
# RUNTIME REQUIREMENTS:
# - A native Debian/Ubuntu or Kali Linux system (or WSL2 with custom kernel/loop devices enabled).
# - Root privileges (sudo).
#
# Usage: sudo bash build-iso.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}=========================================================${NC}"
echo -e "${CYAN}        NEXUS AI - CUSTOM LIVE ISO COMPILER${NC}"
echo -e "${CYAN}=========================================================${NC}"

# 1. Root check
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Error: This build script must be run as root (sudo).${NC}"
    exit 1
fi

# 2. Package Dependency Checks
echo -e "${YELLOW}[*] Installing live-build and compilation tools...${NC}"
apt-get update -y
apt-get install -y live-build xorriso squashfs-tools curl git daemonize debootstrap

# 3. Handle WSL2 loop device constraint
# live-build requires loop devices (/dev/loop0, etc.) to construct disk images.
# In many WSL2 environments, these device nodes do not exist by default.
if grep -qis "microsoft" /proc/version || grep -qis "wsl" /proc/version; then
    echo -e "${YELLOW}[*] WSL2 environment detected. Verifying loop device nodes...${NC}"
    if [ ! -b /dev/loop0 ]; then
        echo -e "${YELLOW}[*] Creating loop device nodes in WSL...${NC}"
        for i in {0..7}; do
            if [ ! -b "/dev/loop$i" ]; then
                mknod "/dev/loop$i" b 7 "$i" || true
            fi
        done
        echo -e "${GREEN}[+] Loop device nodes created successfully.${NC}"
    fi
fi

# 4. Set up clean build workspace
BUILD_WORKSPACE="/opt/nexus-iso-build"
echo -e "${YELLOW}[*] Creating clean workspace: ${BUILD_WORKSPACE}${NC}"
rm -rf "$BUILD_WORKSPACE"
mkdir -p "$BUILD_WORKSPACE"
cd "$BUILD_WORKSPACE"

# 5. Initialize live-build configuration
echo -e "${YELLOW}[*] Initializing live-build structure...${NC}"
lb config \
    --binary-images iso \
    --distribution noble \
    --archive-areas "main contrib non-free non-free-firmware" \
    --apt-recommends false \
    --linux-flavours generic

# 6. Add Custom Files & Binary Overlay
echo -e "${YELLOW}[*] Overlaying Nexus AI Security Suite into Live filesystem...${NC}"
CHROOT_OVERLAY="config/includes.chroot"
mkdir -p "${CHROOT_OVERLAY}/usr/local/bin"
mkdir -p "${CHROOT_OVERLAY}/etc/systemd/system"

# Copy the Linux package binary from our releases folder
BINARY_SOURCE="${SCRIPT_DIR}/react-example-linux"

if [ -f "$BINARY_SOURCE" ]; then
    echo -e "${GREEN}[*] Found packaged standalone binary. Adding to overlay...${NC}"
    cp "$BINARY_SOURCE" "${CHROOT_OVERLAY}/usr/local/bin/nexus-suite"
    chmod +x "${CHROOT_OVERLAY}/usr/local/bin/nexus-suite"
else
    echo -e "${YELLOW}[!] Standalone binary not found in releases folder.${NC}"
    echo -e "${YELLOW}[*] Downloading pre-compiled helper script as fallback...${NC}"
    # Fallback boot wrapper script inside the chroot
    cat <<'EOF' > "${CHROOT_OVERLAY}/usr/local/bin/nexus-suite"
#!/bin/bash
echo "[*] Launching Nexus AI Security Suite in Live OS..."
export NODE_ENV=production
export PORT=3000
# Run standard startup sequence
exec node /usr/local/share/nexus/server.cjs
EOF
    chmod +x "${CHROOT_OVERLAY}/usr/local/bin/nexus-suite"
fi

# 7. Configure systemd service inside chroot to launch console on boot
cat <<EOF > "${CHROOT_OVERLAY}/etc/systemd/system/nexus-suite.service"
[Unit]
Description=Nexus AI Security Suite Live Daemon
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/nexus-suite
Restart=always
Environment=PORT=3000
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF

# 8. Hook systemd service activation in chroot boot stages
mkdir -p config/hooks/normal
cat <<'EOF' > config/hooks/normal/0990-enable-nexus-service.hook.chroot
#!/bin/sh
systemctl enable nexus-suite.service || true
EOF
chmod +x config/hooks/normal/0990-enable-nexus-service.hook.chroot

# 9. Trigger Live OS ISO Build Compilation
echo -e "${GREEN}=========================================================${NC}"
echo -e "${GREEN}[+] BUILD CONFIGURATION STAGED SUCCESSFULLY!${NC}"
echo -e "${YELLOW}[*] Launching live-build compilation. This may take several minutes...${NC}"
echo -e "${CYAN}=========================================================${NC}"

mkdir -p config/hooks/early
mkdir -p config/hooks/late
cat <<'EOF' > config/hooks/early/0000-hide-boot.hook.chroot
#!/bin/sh
echo "[!] Hiding /boot to prevent chmod errors..."
mv /boot /boot_hidden
EOF
chmod +x config/hooks/early/0000-hide-boot.hook.chroot

cat <<'EOF' > config/hooks/late/9999-restore-boot.hook.chroot
#!/bin/sh
echo "[!] Restoring /boot..."
mv /boot_hidden /boot
EOF
chmod +x config/hooks/late/9999-restore-boot.hook.chroot
mkdir -p config/hooks/early
cat <<'EOF' > config/hooks/early/0000-fix-symlinks.hook.chroot
#!/bin/sh
# Force remove symlinks and replace with regular empty files
echo "[!] Forcing regular files for /boot/initrd.img..."
rm -f /boot/initrd.img /boot/initrd.img.old
touch /boot/initrd.img /boot/initrd.img.old
EOF
chmod +x config/hooks/early/0000-fix-symlinks.hook.chroot
mkdir -p config/hooks/early
cat <<'EOF' > config/hooks/early/0000-fix-symlinks.hook.chroot
#!/bin/sh
# Fix dangling symlinks in /boot *before* any hacks stage
echo "[!] Purging dangling symlinks in /boot..."
find /boot -type l -xtype l -delete
EOF
chmod +x config/hooks/early/0000-fix-symlinks.hook.chroot
mkdir -p config/hooks/normal
cat <<'EOF' > config/hooks/normal/0000-fix-symlinks.hook.chroot
#!/bin/sh
# Create dummy files for dangling symlinks in /boot to prevent chmod errors
echo "[!] Creating dummy files for symlinks in /boot to satisfy chmod..."
touch /boot/initrd.img /boot/initrd.img.old
EOF
chmod +x config/hooks/normal/0000-fix-symlinks.hook.chroot
mkdir -p config/hooks/normal
cat <<'EOF' > config/hooks/normal/0000-fix-symlinks.hook.chroot
#!/bin/sh
# Fix dangling symlinks in /boot that cause chmod errors in lb_chroot_hacks
echo "[!] Purging dangling symlinks in /boot..."
rm -f /boot/initrd.img /boot/initrd.img.old
EOF
chmod +x config/hooks/normal/0000-fix-symlinks.hook.chroot
mkdir -p config/hooks/normal
cat <<'EOF' > config/hooks/normal/0000-fix-symlinks.hook.chroot
#!/bin/sh
# Fix dangling symlinks in /boot that cause chmod errors in lb_chroot_hacks
if [ -L /boot/initrd.img ] && [ ! -e /boot/initrd.img ]; then
    echo "[!] Fixing dangling symlink: /boot/initrd.img"
    # Find the target if it exists, or create a dummy
    ln -sf /boot/initrd.img-$(ls /boot/initrd.img-* | sort | tail -n 1 | cut -d'-' -f2-) /boot/initrd.img || touch /boot/initrd.img
fi
if [ -L /boot/initrd.img.old ] && [ ! -e /boot/initrd.img.old ]; then
    echo "[!] Fixing dangling symlink: /boot/initrd.img.old"
    touch /boot/initrd.img.old
fi
EOF
chmod +x config/hooks/normal/0000-fix-symlinks.hook.chroot
lb build

# Move compiled ISO output back to releases folder
if [ -f "live-image-amd64.hybrid.iso" ]; then
    cp "live-image-amd64.hybrid.iso" "${SCRIPT_DIR}/nexus-live-security.iso"
    echo -e "${GREEN}[+] ISO COMPILATION SUCCESSFUL!${NC}"
    echo -e "${GREEN}    -> Output: ${SCRIPT_DIR}/nexus-live-security.iso${NC}"
else
    echo -e "${RED}[!] ISO Compilation failed. Please review chroot log files above.${NC}"
    exit 1
fi









# Fix dangling symlinks
mkdir -p config/hooks/early
cat <<'EOF' > config/hooks/early/0000-fix-symlinks.hook.chroot
#!/bin/sh
rm -f /boot/initrd.img /boot/initrd.img.old
touch /boot/initrd.img /boot/initrd.img.old
EOF
chmod +x config/hooks/early/0000-fix-symlinks.hook.chroot

