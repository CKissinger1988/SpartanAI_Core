#!/bin/bash
# NEXUS // AI - Custom XSession Entry
# This script launches the platform as the primary desktop environment.

# 1. Start Window Manager (Minimal)
openbox &

# 2. Wait for X11 to settle
sleep 2

# 3. Launch Nexus AI in Kiosk/Full-screen mode
# We assume standard user 'kali' or 'root'
cd /opt/nexus-ai
npm start -- --kiosk
