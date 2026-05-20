# NexusAI Security Suite - Simulation Install Script
# Use this to verify the installation logic without modifying the system.

echo "--- Starting NexusAI Installation Simulation ---"

# Mock directories
MOCK_ROOT="./mock_system"
mkdir -p "$MOCK_ROOT/usr/share/xsessions"
mkdir -p "$MOCK_ROOT/usr/local/bin"
mkdir -p "$MOCK_ROOT/etc/nexusai"

echo "[1/4] Simulating Dependency Check..."
echo "  -> Mocking check for nodejs: FOUND"
echo "  -> Mocking check for npm: FOUND"
echo "  -> Mocking check for openbox: FOUND"

echo "[2/4] Simulating Configuration Generation..."
# Generate .desktop entry
echo "[Desktop Entry]
Name=NexusAI
Comment=NexusAI Security Suite Desktop
Exec=/usr/local/bin/nexusai-session.sh
Type=Application" > "$MOCK_ROOT/usr/share/xsessions/nexusai.desktop"
echo "  -> Created mock /usr/share/xsessions/nexusai.desktop"

# Generate session script
echo "#!/bin/bash
openbox &
exec npm start --prefix $(pwd) -- --kiosk" > "$MOCK_ROOT/usr/local/bin/nexusai-session.sh"
chmod +x "$MOCK_ROOT/usr/local/bin/nexusai-session.sh"
echo "  -> Created mock /usr/local/bin/nexusai-session.sh"

echo "[3/4] Simulating Build Process..."
echo "  -> Build verification: SUCCESS"

echo "[4/4] Finalizing Simulation..."
if [ -f "$MOCK_ROOT/usr/share/xsessions/nexusai.desktop" ] && [ -x "$MOCK_ROOT/usr/local/bin/nexusai-session.sh" ]; then
    echo "--- Simulation Complete: SUCCESS ---"
else
    echo "--- Simulation Failed: MISSING FILES ---"
    exit 1
fi
