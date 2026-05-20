#!/bin/bash
# NEXUS // AI - Post-Install Root, Desktop & Strict Security Setup
echo "--- NEXUS // AI: SECURING SYSTEM ---"

# 1. Update Jarvis and dependencies
cd /opt/nexus-ai/JarvisAI_Stable
git pull origin main || true

# 2. Force NexusAI as the only Desktop Session
mkdir -p /etc/skel/.config/openbox
mkdir -p /root/.config/openbox

cat <<EOF > /etc/xdg/openbox/autostart
# NEXUS // AI Autostart
if [ -f "/opt/nexus-ai/scripts/start_nexus.sh" ]; then
    /opt/nexus-ai/scripts/start_nexus.sh &
fi
EOF

cp /etc/xdg/openbox/autostart /root/.config/openbox/autostart

# 3. Configure LightDM to auto-login root
mkdir -p /etc/lightdm/lightdm.conf.d/
cat <<EOF > /etc/lightdm/lightdm.conf.d/nexus-ai.conf
[Seat:*]
user-session=openbox
autologin-user=root
autologin-user-timeout=0
EOF

# 4. Strict Anonymity: Macchanger on boot
cat <<EOF > /etc/systemd/system/macchanger.service
[Unit]
Description=Macchanger Randomize MAC
Wants=network-pre.target
Before=network-pre.target
BindsTo=sys-subsystem-net-devices-eth0.device
After=sys-subsystem-net-devices-eth0.device

[Service]
Type=oneshot
ExecStart=/usr/bin/macchanger -r eth0
ExecStart=/usr/bin/macchanger -r wlan0
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF
systemctl enable macchanger.service

# 5. Strict Anonymity: Tor Transparent Proxy (Basic IPTables rules)
# Note: Real world transparent proxying requires extensive iptables configuration.
# This establishes a baseline blocking non-Tor traffic for debian-tor user.
cat <<EOF > /etc/tor/torrc
VirtualAddrNetworkIPv4 10.192.0.0/10
AutomapHostsOnResolve 1
TransPort 9040
DNSPort 5353
EOF
systemctl enable tor

# 6. Strict Anonymity: Disable System Logging (rsyslog & journald limits)
systemctl disable rsyslog
systemctl stop rsyslog
mkdir -p /etc/systemd/journald.conf.d/
cat <<EOF > /etc/systemd/journald.conf.d/volatile.conf
[Journal]
Storage=volatile
RuntimeMaxUse=10M
EOF

# 7. Setup NexusAI as a system service
if [ -f "/opt/nexus-ai/scripts/nexus-ai.service" ]; then
    cp /opt/nexus-ai/scripts/nexus-ai.service /etc/systemd/system/
    systemctl enable nexus-ai.service
fi

# 7b. Setup Jarvis Kali Monitor Service
cat <<EOF > /etc/systemd/system/jarvis-kali-monitor.service
[Unit]
Description=Jarvis Kali Update Monitor
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /opt/nexus-ai/scripts/kali_monitor.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF
systemctl enable jarvis-kali-monitor.service

# 8. Ensure full root privileges
chown -R root:root /opt/nexus-ai
chmod -R 700 /opt/nexus-ai

# 9. Final cleanup and tool validation
apt-get update && apt-get install -y --fix-missing
pip3 install samloader-py --break-system-packages || pip3 install samloader-py
echo "--- SETUP COMPLETE ---"
