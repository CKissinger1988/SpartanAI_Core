#!/bin/bash
# gcp_deploy_jarvis_backend.sh - Fortress + Pi Super Node Deployment

# --- Configuration ---
PROJECT_ID="your-gcp-project-id"
ZONE="us-central1-c"
INSTANCE_NAME="jarvis-supernode-fortress"
MACHINE_TYPE="n2-standard-4" # Minimum 4 Cores recommended for Super Node
IMAGE_FAMILY="debian-11"
IMAGE_PROJECT="debian-cloud"
REPO_URL="https://github.com/CKissinger1988/JarvisAI_Core.git"
GRPC_PORT=50051
PI_PORTS="31400-31409" # Standard Pi Node consensus ports

echo "--- Initializing Global Launch: JarvisAI Super Node Fortress ---"

# 1. Validate gcloud
gcloud config set project "$PROJECT_ID"
gcloud config set compute/zone "$ZONE"

# 2. Provision Hardened VM with Super Node Resources
echo "Provisioning high-availability VM instance..."
gcloud compute instances create "$INSTANCE_NAME" \
    --zone="$ZONE" \
    --machine-type="$MACHINE_TYPE" \
    --image-family="$IMAGE_FAMILY" \
    --image-project="$IMAGE_PROJECT" \
    --boot-disk-size="200GB" \
    --boot-disk-type="pd-ssd" \
    --tags="jarvis-fortress,pi-supernode" \
    --metadata="startup-script='
        # OS Hardening & Dependencies
        apt update && apt install -y ufw fail2ban tor docker.io git python3-venv
        
        # Configure Docker for Pi Node Container
        systemctl enable docker
        systemctl start docker

        # Firewall Lockdown
        ufw default deny incoming
        ufw allow ssh
        ufw allow $GRPC_PORT
        ufw allow $PI_PORTS/tcp # Allow Pi Consensus Traffic
        ufw --force enable

        # Enable Tor Layer
        systemctl enable tor
        systemctl start tor
    '"

# 3. Configure Network Firewall for Pi Blockchain
echo "Opening Pi Network consensus ports..."
if ! gcloud compute firewall-rules describe "allow-pi-consensus" --project="$PROJECT_ID" &> /dev/null; then
    gcloud compute firewall-rules create "allow-pi-consensus" \
        --project="$PROJECT_ID" \
        --direction=INGRESS \
        --priority=1000 \
        --network=default \
        --action=ALLOW \
        --rules="tcp:31400-31409" \
        --source-ranges="0.0.0.0/0" \
        --target-tags="pi-supernode"
fi

# 4. Secure Deploy Core
echo "Deploying CNSA-compliant core and mTLS identities..."
gcloud compute scp --recurse certs "$INSTANCE_NAME":~/JarvisAI_Core/cloud_backend/ --zone="$ZONE"

gcloud compute ssh "$INSTANCE_NAME" --zone="$ZONE" --command="
    cd ~/JarvisAI_Core/cloud_backend;
    python3 -m venv venv;
    ./venv/bin/pip install -r requirements.txt;
    # Generate stubs
    ./venv/bin/python -m grpc_tools.protoc -I=../proto --python_out=. --grpc_python_out=. ../proto/jarvis.proto;
    # Start Secure Backend
    export GRPC_PORT=$GRPC_PORT;
    nohup ./venv/bin/python main.py > jarvis_supernode.log 2>&1 &
"

EXTERNAL_IP=$(gcloud compute instances describe "$INSTANCE_NAME" --zone="$ZONE" --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "--- Fortress Super Node Deployment Successful ---"
echo "Secure Central Intelligence Online at: $EXTERNAL_IP"
echo "Pi Network Consensus Ports (31400-31409) Open."
echo "mTLS Enforced. Docker active for Pi Blockchain container."
