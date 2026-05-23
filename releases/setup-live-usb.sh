#!/bin/bash
# =========================================================================
#  NEXUS AI SECURITY SUITE - LIVE USB DEPLOYMENT & PERSISTENCE CONFIGURATION
# =========================================================================
# This script sets up the security suite on a Live USB environment (e.g., Kali or Debian Live)
# and registers systemd configuration to run automatically on start.
# Requires root privileges. Run with: sudo bash setup-live-usb.sh

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}=========================================================${NC}"
echo -e "${CYAN}   NEXUS AI SECURITY SUITE - LIVE USB PROVISIONING ENGINE${NC}"
echo -e "${CYAN}=========================================================${NC}"

# 1. Root verification
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Error: This script must be run with sudo/root privileges.${NC}"
    exit 1
fi

# 2. Identify persistence mount point
# Under Kali Live, the persistence partition is usually mounted at /run/live/persistence/sdb2 or similar
# Let's inspect active mounts for persistence
PERSISTENCE_MOUNT=""
if mount | grep -qi "persistence"; then
    PERSISTENCE_MOUNT=$(mount | grep -i "persistence" | awk '{print $3}' | head -n 1)
    echo -e "${GREEN}[*] Detected active persistence partition mounted at: ${PERSISTENCE_MOUNT}${NC}"
    # 2.1 Configure persistence.conf if missing to ensure driver persistence
    if [ ! -f "${PERSISTENCE_MOUNT}/persistence.conf" ]; then
        echo -e "${YELLOW}[*] Initializing persistence configuration for root overlay...${NC}"
        echo "/ union" > "${PERSISTENCE_MOUNT}/persistence.conf"
    fi
else
    echo -e "${YELLOW}[!] Warning: Active persistence partition not found in active mounts.${NC}"
    echo -e "${YELLOW}[*] Continuing configuration in normal live storage layer...${NC}"
fi

# 3. Locate compiled release binary
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
BINARY_PATH="${SCRIPT_DIR}/react-example-linux"

INSTALL_BIN="/usr/local/bin/nexus-suite"

if [ -f "$BINARY_PATH" ]; then
    echo -e "${GREEN}[*] Copying Linux binary to path: ${INSTALL_BIN}${NC}"
    cp "$BINARY_PATH" "$INSTALL_BIN"
    chmod +x "$INSTALL_BIN"
else
    echo -e "${YELLOW}[!] Standalone binary not found. Creating live source boot wrapper...${NC}"
    SRC_DIR="$(cd "${SCRIPT_DIR}/.." &>/dev/null && pwd)"
    cat <<EOF > "$INSTALL_BIN"
#!/bin/bash
export NODE_ENV=production
export PORT=3000
cd "${SRC_DIR}"
exec npm run start
EOF
    chmod +x "$INSTALL_BIN"
fi

# 4. Install supporting security binaries and hardware detection tools
echo -e "${YELLOW}[*] Updating system dependencies and hardware tools...${NC}"
apt-get update -y || true
apt-get install -y nmap daemonize iptables curl lshw usbutils pciutils dkms firmware-linux || true

# 5. Hardware Detection & Driver Provisioning
echo -e "${YELLOW}[*] Probing hardware architecture for driver matching...${NC}"
# Detect GPU (NVIDIA check)
if lspci | grep -qi "nvidia"; then
    echo -e "${GREEN}[+] NVIDIA GPU detected. Provisioning proprietary drivers...${NC}"
    apt-get install -y nvidia-detect nvidia-kernel-dkms || true
fi

# Detect Wireless
if lspci | grep -qi "wireless" || lsusb | grep -qi "wireless"; then
    echo -e "${GREEN}[+] Wireless hardware detected. Updating firmware packages...${NC}"
    apt-get install -y firmware-realtek firmware-atheros firmware-liberation || true
fi

# 6. Create autostart Systemd service
SERVICE_PATH="/etc/systemd/system/nexus-suite.service"
echo -e "${YELLOW}[*] Registering systemd startup daemon: ${SERVICE_PATH}${NC}"

cat <<EOF > "$SERVICE_PATH"
[Unit]
Description=Nexus AI Security Suite Boot Console
After=network.target

[Service]
Type=simple
ExecStart=$INSTALL_BIN
Restart=always
RestartSec=5
Environment=PORT=3000
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF

# 7. Enable the boot service
echo -e "${YELLOW}[*] Activating system startup hooks...${NC}"
systemctl daemon-reload
systemctl enable nexus-suite.service || true
systemctl restart nexus-suite.service || true

# 8. Configure iptables to redirect standard HTTP traffic (optional, port 80 to 3000)
# This makes it easier to access when booting headless on live usb
echo -e "${YELLOW}[*] Applying iptables routing checks...${NC}"
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 3000 || true

echo -e "${CYAN}=========================================================${NC}"
echo -e "${GREEN}[+] LIVE USB PERSISTENCE INSTALL COMPLETED!${NC}"
echo -e "${GREEN}    -> Status: Standalone boot service enabled.${NC}"
echo -e "${GREEN}    -> Target Port: http://localhost:3000/${NC}"
echo -e "${GREEN}    -> CLI Access command: sudo systemctl status nexus-suite${NC}"
echo -e "${CYAN}=========================================================${NC}"
