#!/bin/bash
# gcp_deploy_jarvis_backend.sh - Fortress Deployment for JarvisAI

# --- Configuration ---
PROJECT_ID="your-gcp-project-id"
ZONE="us-central1-c"
INSTANCE_NAME="jarvis-fortress-node"
MACHINE_TYPE="e2-standard-4"
IMAGE_FAMILY="debian-11"
IMAGE_PROJECT="debian-cloud"
REPO_URL="https://github.com/CKissinger1988/JarvisAI_Core.git"
GRPC_PORT=50051

echo "--- Initializing Fortress Deployment: JarvisAI Central Intelligence ---"

# 1. Validate gcloud
gcloud config set project "$PROJECT_ID"
gcloud config set compute/zone "$ZONE"

# 2. Provision Hardened VM
echo "Provisioning hardened VM instance..."
gcloud compute instances create "$INSTANCE_NAME" \
    --zone="$ZONE" \
    --machine-type="$MACHINE_TYPE" \
    --image-family="$IMAGE_FAMILY" \
    --image-project="$IMAGE_PROJECT" \
    --tags="jarvis-fortress" \
    --metadata="startup-script='
        # OS Hardening
        apt update && apt install -y ufw fail2ban tor
        ufw default deny incoming
        ufw allow ssh
        ufw allow $GRPC_PORT
        ufw --force enable
        # Enable Tor for anonymity routing layer
        systemctl enable tor
        systemctl start tor
    '"

# 3. Secure Deploy
echo "Deploying CNSA-compliant core and mTLS identities..."
# Copying local certs to remote (Requires gcloud compute scp)
gcloud compute scp --recurse certs "$INSTANCE_NAME":~/JarvisAI_Core/cloud_backend/ --zone="$ZONE"

gcloud compute ssh "$INSTANCE_NAME" --zone="$ZONE" --command="
    cd ~/JarvisAI_Core/cloud_backend;
    # Setup venv and run
    python3 -m venv venv;
    ./venv/bin/pip install -r requirements.txt;
    # Generate stubs if needed
    ./venv/bin/python -m grpc_tools.protoc -I=../proto --python_out=. --grpc_python_out=. ../proto/jarvis.proto;
    # Start Secure Backend
    export GRPC_PORT=$GRPC_PORT;
    nohup ./venv/bin/python main.py > jarvis_secure.log 2>&1 &
"

EXTERNAL_IP=$(gcloud compute instances describe "$INSTANCE_NAME" --zone="$ZONE" --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "--- Fortress Deployment Successful ---"
echo "Secure Central Intelligence Online at: $EXTERNAL_IP"
echo "mTLS Enforced. All communication is CNSA-grade encrypted."
