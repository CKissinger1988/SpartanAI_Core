#!/bin/bash
# SentinelAI v50-Supreme Init Script
MODE="server"
if [ -f /proc/cmdline ]; then
    MODE=$(cat /proc/cmdline | sed 's/.*sentinel_mode=\([^ ]*\).*/\1/')
fi

if [ "$MODE" == "install" ]; then
    python3 /backend/core/PersistenceShards/autonomous_installer.py
elif [ "$MODE" == "kiosk" ]; then
    python3 /backend/core/PersistenceShards/kiosk_controller.py
elif [ "$MODE" == "desktop" ]; then
    python3 /backend/qt6_dashboard.py
else
    python3 /backend/core/CognitiveCore/jarvis.py
fi
