#!/bin/bash
set -e

echo "========================================================="
echo "        SPARTANAI GCP DOCKER BUILD ENGINE                "
echo "========================================================="

echo "[*] Ensuring Docker is installed..."
if ! command -v docker &> /dev/null; then
    echo "[!] Docker not found. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
fi

if ! command -v docker-compose &> /dev/null; then
    echo "[!] Docker Compose not found. Installing..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

echo "[*] Building SpartanAI Docker Image..."
# We assume this is run from the project root
docker build -t spartanai-cortex:latest .

echo "[+] Docker Image 'spartanai-cortex:latest' compiled successfully."
echo "[*] To deploy on GCP, run: docker-compose up -d"
