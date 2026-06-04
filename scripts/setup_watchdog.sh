#!/bin/bash
# Sets up a cron-based watchdog to ensure AI Supreme is always running

WATCHDOG_SCRIPT="/usr/local/bin/ai-watchdog.sh"

echo "[*] Installing Watchdog Script..."
cat << 'EOF' | sudo tee "$WATCHDOG_SCRIPT" > /dev/null
#!/bin/bash
if ! systemctl is-active --quiet ai-supreme-boot.service; then
    echo "[$(date)] Watchdog: ai-supreme-boot offline. Initiating ai-start..." >> /var/log/ai-watchdog.log
    systemctl start ai-supreme-boot.service
fi
EOF
sudo chmod +x "$WATCHDOG_SCRIPT"

echo "[*] Adding to crontab (runs every 5 minutes)..."
(crontab -l 2>/dev/null | grep -v "$WATCHDOG_SCRIPT"; echo "*/5 * * * * $WATCHDOG_SCRIPT") | crontab -

echo -e "\033[92m[+] Watchdog successfully installed and activated!\033[0m"