#version=RHEL9
# JarvisAI Custom OS based on Red Hat Enterprise Linux AI
# Unattended Installation Configuration

text
cdrom
lang en_US.UTF-8
keyboard us
timezone UTC
rootpw --plaintext nexus_admin_override
user --name=creator --password=creator_override --groups=wheel

# Network & Services
network --bootproto=dhcp --onboot=yes --activate
firewall --enabled --ssh --port=50051:tcp,31400-31409:tcp
services --enabled=sshd,docker,tor

# Partitioning
zerombr
clearpart --all --initlabel
autopart --type=lvm

%packages
@^minimal-environment
@development
git
python3
python3-pip
docker-ce
docker-ce-cli
containerd.io
docker-compose-plugin
tor
ufw
fail2ban
dos2unix
%end

%post --log=/var/log/jarvis_install.log
#!/bin/bash
echo "--- Initializing JarvisAI RHEL AI OS ---"

# Start and enable core services
systemctl enable docker
systemctl enable tor

# Clone Supreme Core
git clone https://github.com/CKissinger1988/JarvisAI_Core.git /opt/JarvisAI_Core
cd /opt/JarvisAI_Core/cloud_backend

# Setup Python Environment for Stubs & Key Generation
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install grpcio-tools cryptography

# Generate Stubs
python3 -m grpc_tools.protoc -I=../proto --python_out=. --grpc_python_out=. ../proto/jarvis.proto
python3 -m grpc_tools.protoc -I=../proto --python_out=. --grpc_python_out=. ../proto/vault.proto

# Create Vault Keys and persist securely for systemd
export VAULT_KEY_LIGHT=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
export VAULT_KEY_SHADOW=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

# Ensure required directories exist
mkdir -p certs knowledge evolution

# Write environment file
cat <<EOF > /etc/jarvis.env
VAULT_KEY_LIGHT=$VAULT_KEY_LIGHT
VAULT_KEY_SHADOW=$VAULT_KEY_SHADOW
GRPC_PORT=50051
MASTER_ADMIN_KEY=nexus_master_override_2026
EOF
chmod 600 /etc/jarvis.env

# Setup systemd service for multi-container Vault architecture
cat <<EOF > /etc/systemd/system/jarvis-core.service
[Unit]
Description=JarvisAI Supreme Core (Docker Compose)
Requires=docker.service
After=docker.service network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/JarvisAI_Core/cloud_backend
EnvironmentFile=/etc/jarvis.env
ExecStart=/usr/bin/docker compose up -d --build
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
EOF

systemctl enable jarvis-core.service

echo "JarvisAI Base OS Installation Complete. Ready for Out-Of-The-Box Execution."
%end
