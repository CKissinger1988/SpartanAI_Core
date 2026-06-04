#!/bin/bash
# =========================================================================
#  AI SUPREME - MAINTENANCE SHUTDOWN SEQUENCE
# =========================================================================
# Safely spins down all AI Supreme services for system maintenance.
# Run this script with sudo from anywhere.

echo -e "\033[93m[*] Initiating Maintenance Shutdown Sequence...\033[0m"

# 0. Backup Autonomous SOC State
echo "[*] Securing backup of SpartanAI SOC databases..."
BACKUP_DIR="/opt/SpartanAI_Security_Core/backups"
sudo mkdir -p "$BACKUP_DIR"
sudo tar -czf "$BACKUP_DIR/soc_state_$(date +%Y%m%d_%H%M%S).tar.gz" -C /opt/SpartanAI_Security_Core . --exclude='.venv' --exclude='.git' 2>/dev/null || true
echo -e "\033[92m    -> Backup secured in $BACKUP_DIR\033[0m"

# 1. Stop Node Orchestrator & Master Boot Service
echo "[*] Stopping Node Orchestrator & Boot Service..."
sudo systemctl stop ai-supreme-boot.service

# 2. Stop Autonomous SOC
echo "[*] Stopping SpartanAI Autonomous SOC..."
sudo systemctl stop spartan-soc-dashboard.service
sudo systemctl stop spartan-soc.service

# 3. Stop Stealth & Traffic Morphing
echo "[*] Stopping Stealth & Identity Services..."
sudo systemctl stop ai-identity-rotate.service 2>/dev/null || true
sudo systemctl stop ai-shadow-chaff.service 2>/dev/null || true
sudo systemctl stop ai-onion-rotate.timer 2>/dev/null || true

# 4. Stop Tor Hidden Services
echo "[*] Stopping Tor Daemon..."
sudo systemctl stop tor.service

# 5. Stop Fail2ban (Leaves UFW active for baseline protection)
echo "[*] Stopping Fail2ban..."
sudo systemctl stop fail2ban.service

echo -e "\033[92m[+] All AI Supreme services successfully stopped. Server is safe for maintenance.\033[0m"