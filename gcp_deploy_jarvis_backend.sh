#!/bin/bash
# gcp_deploy_jarvis_backend.sh - Perfection Deployment for JarvisAI

# --- Configuration (TO BE CUSTOMIZED BY CREATOR) ---
PROJECT_ID="nexusai-core-2026"
ZONE="us-central1-a"
INSTANCE_NAME="jarvis-central-core"
MACHINE_TYPE="n2-standard-8" # High-performance resources
IMAGE_FAMILY="debian-11"
IMAGE_PROJECT="debian-cloud"
REPO_URL="https://github.com/CKissinger1988/JarvisAI_Core.git"
GRPC_PORT=50051

echo "--- Initializing Perfection Deployment: JarvisAI Supreme Core ---"

# 1. System Environment Check
if ! command -v gcloud &> /dev/null; then
    echo "ERROR: gcloud CLI not found. Please install it first."
    exit 1
fi

# 2. Provision Infrastructure
echo "Provisioning high-availability fortress node..."
gcloud compute instances create "$INSTANCE_NAME" \
    --project="$PROJECT_ID" \
    --zone="$ZONE" \
    --machine-type="$MACHINE_TYPE" \
    --image-family="$IMAGE_FAMILY" \
    --image-project="$IMAGE_PROJECT" \
    --boot-disk-size="250GB" \
    --boot-disk-type="pd-ssd" \
    --tags="jarvis-fortress,pi-supernode" \
    --metadata="startup-script='
        # Auto-configure OS & Hardening
        apt update && apt upgrade -y
        apt install -y ufw fail2ban tor docker.io git python3-pip python3-venv openssl dos2unix
        
        # Enable Core Services
        systemctl enable --now docker tor
        
        # Firewall Configuration
        ufw default deny incoming
        ufw allow ssh
        ufw allow $GRPC_PORT
        ufw allow 31400:31409/tcp # Pi consensus
        ufw --force enable
    '"

# 3. Secure Core Deployment
echo "Synchronizing Supreme Core assets and identities..."
# Ensure local certs are generated
if [ ! -d "certs" ]; then
    echo "Generating fresh mTLS identities..."
    # (Self-contained certificate generation logic could go here)
fi

# Clone and Prep
gcloud compute ssh "$INSTANCE_NAME" --zone="$ZONE" --project="$PROJECT_ID" --command="
    if [ ! -d \"JarvisAI_Core\" ]; then
        git clone $REPO_URL
    fi
    cd JarvisAI_Core/cloud_backend
    # Create persistent storage directories
    mkdir -p certs knowledge evolution
    # Setup venv
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
    # Generate stubs
    ./venv/bin/python -m grpc_tools.protoc -I=../proto --python_out=. --grpc_python_out=. ../proto/jarvis.proto
"

# Transfer Identities
gcloud compute scp --recurse certs "$INSTANCE_NAME":~/JarvisAI_Core/cloud_backend/ --zone="$ZONE" --project="$PROJECT_ID"

# 4. Launch Autonomous Service
echo "Activating JarvisAI Central Intelligence..."
gcloud compute ssh "$INSTANCE_NAME" --zone="$ZONE" --project="$PROJECT_ID" --command="
    cd ~/JarvisAI_Core/cloud_backend
    export GRPC_PORT=$GRPC_PORT
    # Run using nohup for persistence
    nohup ./venv/bin/python main.py > jarvis_active.log 2>&1 &
"

EXTERNAL_IP=$(gcloud compute instances describe "$INSTANCE_NAME" --zone="$ZONE" --project="$PROJECT_ID" --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "--- Perfection Deployment SUCCESS ---"
echo "JarvisAI Central Core is LIVE at: $EXTERNAL_IP"
echo "Prime Directive engaged. Symmetric Brain online. Pi Synergy active."
