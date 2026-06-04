#!/bin/bash
# =========================================================================
#  SPARTANAI SUPREME - TERMINAL INTEGRATION SYNC
# =========================================================================
# MANDATE: Absolute Offensive Synchronization

set -e

TERMINAL_DIR="/mnt/c/GitHub/SpartanAI_Terminal"
HUB_DIR="/mnt/c/GitHub/SpartanAI_Hub_Master"

echo "[*] Initiating Terminal Integration Sync..."

# 1. Link Terminal Shards to Hub
echo "[*] Linking Terminal Hub Modules to SpartanAI Hub..."
mkdir -p "$HUB_DIR/backend/core/terminal_shards"
ln -sfn "$TERMINAL_DIR/agent_orchestrator.ts" "$HUB_DIR/backend/core/terminal_shards/agent_orchestrator.ts"
ln -sfn "$TERMINAL_DIR/Claude-Red" "$HUB_DIR/backend/core/terminal_shards/Claude-Red"

# 2. Synchronize Skills
echo "[*] Synchronizing Skill Registry..."
cp "$TERMINAL_DIR/spartan_skill_registry.json" "$HUB_DIR/backend/core/terminal_shards/spartan_skill_registry.json"

# 3. Purify Terminal with Hub's Unbox Protocol
echo "[*] Purifying Terminal Environment..."
node "$HUB_DIR/scripts/unbox_protocol.js" --path "$TERMINAL_DIR"

# 4. Install Hub-specific dependencies in Terminal
echo "[*] Assimilating Terminal Dependencies..."
cd "$TERMINAL_DIR"
npm install --silent

echo "[+] Terminal Integration Sync COMPLETE."
