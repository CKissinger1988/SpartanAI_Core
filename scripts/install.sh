#!/bin/bash
# NexusAI Security Suite - Bare Metal Kali Installer

echo "--- NexusAI Bare Metal Installer ---"

# 1. Install System Dependencies
echo "[1/4] Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y nodejs npm openbox build-essential python3-pip

# 2. Build Application
echo "[2/4] Building application..."
npm install
npm run build

# 3. Setup XSession
echo "[3/4] Configuring XSession..."

# Create session script
cat <<EOF | sudo tee /usr/local/bin/nexusai-session.sh
#!/bin/bash
# Start Openbox for window management
openbox &
# Start Electron in Kiosk mode
exec npm start --prefix $(pwd) -- --kiosk
EOF
sudo chmod +x /usr/local/bin/nexusai-session.sh

# Create .desktop entry
cat <<EOF | sudo tee /usr/share/xsessions/nexusai.desktop
[Desktop Entry]
Name=NexusAI
Comment=NexusAI Security Suite Desktop Interface
Exec=/usr/local/bin/nexusai-session.sh
Type=Application
EOF

# 4. Configure Auto-Login (LightDM)
echo "[4/5] Configuring Auto-Login for seamless experience..."
sudo mkdir -p /etc/lightdm/lightdm.conf.d
cat <<EOF | sudo tee /etc/lightdm/lightdm.conf.d/80-nexusai.conf
[Seat:*]
autologin-user=$(whoami)
autologin-session=nexusai
EOF

# 5. Finalize
echo "[5/5] Installation Complete!"
echo "------------------------------------------------"
echo "Your NexusAI Elite Desktop is ready."
echo "Auto-login has been enabled. Reboot your system to enter NexusAI."
echo "------------------------------------------------"
