#!/bin/bash
# Configures ai_supreme_boot.sh to run automatically on system boot.
# Run this script with sudo from the root of the repository.

REPO_DIR=$(pwd)
SERVICE_FILE="/etc/systemd/system/ai-supreme-boot.service"

echo "[*] Creating systemd service for AI Supreme Boot Sequence..."

cat <<EOF | sudo tee "$SERVICE_FILE" > /dev/null
[Unit]
Description=AI Supreme Omnipotent Boot Sequence
After=network.target tor.service

[Service]
Type=simple
User=root
WorkingDirectory=$REPO_DIR
ExecStart=/bin/bash $REPO_DIR/ai_supreme_boot.sh
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "[*] Injecting global bash aliases..."
cat <<EOF | sudo tee /etc/profile.d/ai-supreme-aliases.sh > /dev/null
alias ai-start="sudo systemctl start ai-supreme-boot.service"
alias ai-stop="sudo bash $REPO_DIR/scripts/maintenance_stop.sh"
alias ai-status="sudo systemctl status ai-supreme-boot.service"
EOF
sudo chmod +x /etc/profile.d/ai-supreme-aliases.sh

echo "[*] Reloading systemd daemon..."
sudo systemctl daemon-reload
sudo systemctl enable ai-supreme-boot.service

echo -e "\033[92m[+] Boot service successfully installed and enabled!\033[0m"
echo "    You can now manage the system globally using:"
echo "      ai-start | ai-stop | ai-status"