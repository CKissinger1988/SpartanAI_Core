#!/bin/bash
# deploy_backend.sh - Automated JarvisAI Linux Backend Installer
set -e

echo "--- JarvisAI Linux Backend Deployment ---"

# 1. Update and install dependencies
sudo apt update && sudo apt install -y python3-pip python3-venv git dos2unix

# 2. Setup directory
mkdir -p ~/jarvis_backend
cd ~/jarvis_backend

# 3. Assuming files are uploaded or cloned here
# If cloning: git clone git@gitlab.com:default173321/nexusai-security-suite.git .

# 4. Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Installing defaults..."
    pip install grpcio grpcio-tools fastapi uvicorn
fi

# 6. Run the backend (using nohup for background persistence)
echo "Starting JarvisAI Backend..."
nohup python3 main.py > jarvis_backend.log 2>&1 &

echo "Deployment Complete. Backend is running in the background."
