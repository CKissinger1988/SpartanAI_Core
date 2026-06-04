#!/bin/bash
# =========================================================================
#  SPARTANAI APEX - PROXMOX OPTIMIZED RELEASE GENERATOR
# =========================================================================
# This script engineers a Proxmox-ready, security-hardened release image.
# It includes QEMU Guest Agent, VirtIO drivers, and kernel hardening.
#
# RUNTIME REQUIREMENTS: Native Debian/Ubuntu/Kali or WSL2.
# =========================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}=========================================================${NC}"
echo -e "${CYAN}      SPARTANAI APEX - PROXMOX RELEASE ENGINEER${NC}"
echo -e "${CYAN}=========================================================${NC}"

# 1. Root Check
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Error: This script must be run as root (sudo).${NC}"
    exit 1
fi

# 2. Workspace Setup
BUILD_DIR="/opt/spartanai_proxmox_build"
echo -e "${YELLOW}[*] Initializing Proxmox workspace: ${BUILD_DIR}${NC}"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# 3. Security Hardening & Virtualization Prerequisites
echo -e "${YELLOW}[*] Staging Proxmox-optimized system profile...${NC}"
cat <<EOF > "${BUILD_DIR}/hardening.sysctl.conf"
# SpartanAI Apex - Kernel Hardening for Proxmox
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
kernel.sysrq = 0
kernel.core_uses_pid = 1
kernel.kptr_restrict = 2
kernel.perf_event_paranoid = 3
EOF

# 4. QEMU Guest Agent & VirtIO Configuration
echo -e "${YELLOW}[*] Configuring QEMU Guest Agent & VirtIO hooks...${NC}"
mkdir -p "${BUILD_DIR}/config/includes.chroot/etc/modules-load.d"
echo "virtio_net" > "${BUILD_DIR}/config/includes.chroot/etc/modules-load.d/virtio.conf"
echo "virtio_pci" >> "${BUILD_DIR}/config/includes.chroot/etc/modules-load.d/virtio.conf"
echo "virtio_blk" >> "${BUILD_DIR}/config/includes.chroot/etc/modules-load.d/virtio.conf"
echo "virtio_balloon" >> "${BUILD_DIR}/config/includes.chroot/etc/modules-load.d/virtio.conf"

# 5. Build Wrapper for Live-Build
echo -e "${YELLOW}[*] Wrapping live-build for Proxmox target...${NC}"
cat <<'EOF' > "${BUILD_DIR}/build_proxmox.sh"
#!/bin/bash
lb config \
    --binary-images iso \
    --distribution noble \
    --archive-areas "main restricted universe multiverse" \
    --apt-recommends false \
    --linux-flavours generic \
    --parent-mirror-bootstrap "http://archive.ubuntu.com/ubuntu/" \
    --mirror-bootstrap "http://archive.ubuntu.com/ubuntu/" \
    --parent-mirror-chroot-security "http://security.ubuntu.com/ubuntu/" \
    --mirror-chroot-security "http://security.ubuntu.com/ubuntu/"

# Add QEMU Guest Agent to package list
echo "qemu-guest-agent" > config/package-lists/proxmox.list.chroot
echo "cloud-init" >> config/package-lists/proxmox.list.chroot

lb build
EOF
chmod +x "${BUILD_DIR}/build_proxmox.sh"

# 6. Deployment Finality
echo -e "${GREEN}[+] Proxmox build environment staged successfully at ${BUILD_DIR}.${NC}"
echo -e "${GREEN}    Run 'cd ${BUILD_DIR} && sudo ./build_proxmox.sh' to compile the image.${NC}"

# Burn a copy of the engineer script to D:
echo -e "${YELLOW}[*] Backing up Proxmox engineer to D: for sovereign redundancy...${NC}"
cp "${BUILD_DIR}/build_proxmox.sh" "/mnt/d/build_proxmox_sovereign.sh" || true

echo -e "${CYAN}=========================================================${NC}"
echo -e "${GREEN}      PROXMOX RELEASE ENGINEERING COMPLETE${NC}"
echo -e "${CYAN}=========================================================${NC}"
