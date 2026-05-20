#!/data/data/com.termux/files/usr/bin/bash
# NEXUS // AI - Termux Mobile Backend Setup
# This script configures the NexusAI backend to run natively on Android via Termux.

set -e

echo "--- NEXUS // AI: MOBILE BACKEND INITIALIZATION ---"

# 1. Update Termux Repositories
echo "[+] Updating Termux environment..."
pkg update -y
pkg upgrade -y

# 2. Install Core Dependencies
echo "[+] Installing core packages (Python, Node.js, Git, Tor, Nmap)..."
pkg install -y python nodejs git tor nmap curl openssh termux-api

# 3. Setup Python Virtual Environment
echo "[+] Configuring Python environment..."
python -m venv $HOME/nexus-venv
source $HOME/nexus-venv/bin/activate

# 4. Install Project Requirements
# We use a modified requirements list to avoid heavy build dependencies in Termux where possible
pip install --upgrade pip
pip install cryptography httpx zeroconf paho-mqtt pycryptodome argon2-cffi fastmcp

# 5. Configure Jarvis for Mobile
echo "[+] Initializing Jarvis Mobile Core..."
mkdir -p $HOME/nexus-ai/data
mkdir -p $HOME/nexus-ai/scripts

# Copy essential scripts from the current directory (assuming cloned)
# In a real Termux env, the user would clone the repo first.
# This script acts as the "bootstrap" after cloning.

# 6. Setup Tor for Mobile Anonymity
echo "[+] Configuring Tor hidden service for mobile C2..."
if [ ! -f "$HOME/.termux/boot/start-tor" ]; then
    mkdir -p $HOME/.termux/boot
    echo "tor &" > $HOME/.termux/boot/start-tor
    chmod +x $HOME/.termux/boot/start-tor
fi

# 7. Create Mobile Launch Script
cat <<EOF > $HOME/nexus-launch.sh
#!/data/data/com.termux/files/usr/bin/bash
source $HOME/nexus-venv/bin/activate
echo "--- NEXUS // AI MOBILE CORE ONLINE ---"
python $HOME/nexus-ai/scripts/kali_monitor.py &
# Start the MCP server for remote management
python $HOME/nexus-ai/scripts/nexus_mcp.py
EOF
chmod +x $HOME/nexus-launch.sh

echo "--- SETUP COMPLETE ---"
echo "To start the NexusAI Mobile Backend, run: ./nexus-launch.sh"
echo "Note: Use the Termux:API app for hardware-level sensor integration."
