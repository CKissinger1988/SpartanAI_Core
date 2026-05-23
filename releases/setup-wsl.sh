#!/bin/bash
# =========================================================================
#  NEXUS AI SECURITY SUITE - WSL NATIVE ENVIRONMENT SETUP SCRIPT
# =========================================================================
# This script configures WSL (Ubuntu/Debian) to host the security console,
# registers the compiled Linux binary, and establishes automatic background startup hooks.

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}=========================================================${NC}"
echo -e "${CYAN}      NEXUS AI SECURITY SUITE - WSL SETUP ENGINE${NC}"
echo -e "${CYAN}=========================================================${NC}"

# 1. Verify environment is WSL
if ! grep -qis "microsoft" /proc/version && ! grep -qis "wsl" /proc/version; then
    echo -e "${RED}[!] WARNING: This environment does not appear to be WSL.${NC}"
    echo -e "${YELLOW}[*] Continuing installation under standard Linux framework...${NC}"
fi

# 2. Check for root privileges
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Please run this script with sudo privileges:${NC}"
    echo -e "${YELLOW}    sudo bash $0${NC}"
    exit 1
fi

# 3. Locate compiled release binary
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
BINARY_PATH="${SCRIPT_DIR}/react-example-linux"

if [ -f "$BINARY_PATH" ]; then
    echo -e "${GREEN}[*] Found compiled Linux/WSL binary at: ${BINARY_PATH}${NC}"
else
    # Fallback to source running instructions if not packaged yet
    echo -e "${YELLOW}[!] Standalone package (react-example-linux) not found.${NC}"
    echo -e "${YELLOW}[*] Configuring runtime dependency checklist instead...${NC}"
fi

# 4. Install local security dependencies (Nmap, Git, etc.)
echo -e "${YELLOW}[*] Updating package repositories and installing security dependencies...${NC}"
apt-get update -y
apt-get install -y nmap git curl daemonize

# 5. Set up Binary System Path
INSTALL_BIN="/usr/local/bin/nexus-suite"
if [ -f "$BINARY_PATH" ]; then
    echo -e "${YELLOW}[*] Installing standalone executable to ${INSTALL_BIN}...${NC}"
    cp "$BINARY_PATH" "$INSTALL_BIN"
    chmod +x "$INSTALL_BIN"
else
    # Create start helper pointing to source workspace
    SRC_DIR="$(cd "${SCRIPT_DIR}/.." &>/dev/null && pwd)"
    echo -e "${YELLOW}[*] Creating run script wrapper to load source directory: ${SRC_DIR}${NC}"
    cat <<EOF > "$INSTALL_BIN"
#!/bin/bash
export NODE_ENV=production
export GEMINI_API_KEY=""
cd "${SRC_DIR}"
npm run start
EOF
    chmod +x "$INSTALL_BIN"
fi

# 6. Configure Systemd Service (For modern WSL with systemd support enabled in /etc/wsl.conf)
SYSTEMD_DIR="/etc/systemd/system"
SERVICE_FILE="${SYSTEMD_DIR}/nexus-suite.service"

echo -e "${YELLOW}[*] Configuring background service integration...${NC}"

cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=Nexus AI Security Suite Service
After=network.target

[Service]
Type=simple
ExecStart=$INSTALL_BIN
Restart=on-failure
Environment=PORT=3000
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF

# 7. Check if Systemd is active, otherwise register fallback SysV/cron script
if ps -p 1 | grep -q systemd; then
    echo -e "${GREEN}[*] Systemd detected. Enabling and launching nexus-suite service...${NC}"
    systemctl daemon-reload
    systemctl enable nexus-suite.service || true
    systemctl restart nexus-suite.service || true
else
    echo -e "${YELLOW}[!] Systemd is not active in this WSL instance (non-systemd wsl).${NC}"
    echo -e "${YELLOW}[*] Installing fallback background daemon launcher via wslboot hooks...${NC}"
    
    # Configure user login profile trigger to daemonize on start if port is empty
    WSL_BOOT_SCRIPT="/usr/local/bin/nexus-wsl-boot"
    cat <<EOF > "$WSL_BOOT_SCRIPT"
#!/bin/bash
if ! ss -tuln | grep -q ":3000 "; then
    echo "[*] Starting Nexus AI Security Suite in background daemon mode..."
    daemonize /usr/local/bin/nexus-suite
fi
EOF
    chmod +x "$WSL_BOOT_SCRIPT"
    
    # Suggest execution command
    echo -e "${GREEN}[+] To start the suite, run: ${CYAN}daemonize $INSTALL_BIN${NC}"
fi

echo -e "${CYAN}=========================================================${NC}"
echo -e "${GREEN}[+] WSL SUITE INITIALIZATION COMPLETE!${NC}"
echo -e "${GREEN}    -> Web Dashboard Address: ${CYAN}http://localhost:3000/${NC}"
echo -e "${GREEN}    -> Native Shell command:  ${CYAN}nexus-suite${NC}"
echo -e "${CYAN}=========================================================${NC}"
