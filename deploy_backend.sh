#!/bin/bash
# deploy_backend.sh - Automated JarvisAI Linux Backend Installer (Docker Compose)
set -e

echo "--- JarvisAI Linux Backend Deployment (Multi-Container Vault System) ---"

# 1. Update and install dependencies
sudo apt update && sudo apt install -y python3-pip python3-venv git dos2unix docker.io docker-compose

# Enable Docker
sudo systemctl enable --now docker

# 2. Setup directory
mkdir -p ~/jarvis_backend
cd ~/jarvis_backend

# 3. Assuming files are uploaded or cloned here
# If cloning: git clone git@gitlab.com:default173321/nexusai-security-suite.git .

# 4. Set up virtual environment to generate stubs
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install grpcio grpcio-tools cryptography

# 5. Generate stubs
python3 -m grpc_tools.protoc -I=../proto --python_out=cloud_backend/ --grpc_python_out=cloud_backend/ ../proto/jarvis.proto
python3 -m grpc_tools.protoc -I=../proto --python_out=cloud_backend/ --grpc_python_out=cloud_backend/ ../proto/vault.proto

# 6. Generate Vault Keys
export VAULT_KEY_LIGHT=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
export VAULT_KEY_SHADOW=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

# 7. Run the backend stack
echo "Starting JarvisAI Backend via Docker Compose..."
cd cloud_backend
sudo docker-compose build
sudo -E docker-compose up -d

echo "Deployment Complete. The Encrypted Vault Backend is running."
