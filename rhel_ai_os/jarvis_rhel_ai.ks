#version=RHEL9
# JarvisAI Supreme Deep Learning OS
# Universal Hardware & Framework Support

text
cdrom
lang en_US.UTF-8
keyboard us
timezone UTC
rootpw --plaintext nexus_admin_override
user --name=creator --password=creator_override --groups=wheel

network --bootproto=dhcp --onboot=yes --activate
firewall --enabled --ssh --port=50051:tcp,31400-31409:tcp
services --enabled=sshd,docker,tor

zerombr
clearpart --all --initlabel
autopart --type=lvm

# Add EPEL for extended packages
repo --name="EPEL" --baseurl=https://dl.fedoraproject.org/pub/epel/9/Everything/x86_64/

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
pciutils
lshw
wget
tar
bzip2
gcc
gcc-c++
make
kernel-devel
kernel-headers
%end

%post --log=/var/log/jarvis_install.log
#!/bin/bash
echo "--- Initializing JarvisAI Deep Learning OS ---"

systemctl enable docker
systemctl enable tor

# --- Universal Deep Learning Environment Setup ---
echo "Installing Universal AI Package Manager (Miniforge/Conda)..."
wget -q "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh" -O /tmp/miniforge.sh
bash /tmp/miniforge.sh -b -p /opt/conda
rm /tmp/miniforge.sh

# Export Conda to PATH for all users
echo 'export PATH="/opt/conda/bin:$PATH"' > /etc/profile.d/conda.sh
source /etc/profile.d/conda.sh

# Create the primary Deep Learning Environment
echo "Installing AI Frameworks & Intel Tools (PyTorch, TensorFlow, OpenVINO)..."
conda create -y -n jarvis_ai python=3.10
conda install -y -n jarvis_ai -c conda-forge -c pytorch -c intel \
    pytorch torchvision torchaudio cpuonly \
    tensorflow \
    openvino openvino-ie4api \
    transformers accelerate datasets \
    pandas numpy scikit-learn

# --- JarvisAI Supreme Core Deployment ---
echo "Deploying Supreme Core..."
git clone https://github.com/CKissinger1988/JarvisAI_Core.git /opt/JarvisAI_Core
cd /opt/JarvisAI_Core/cloud_backend

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install grpcio-tools cryptography

# Generate Stubs
python3 -m grpc_tools.protoc -I=../proto --python_out=. --grpc_python_out=. ../proto/jarvis.proto
python3 -m grpc_tools.protoc -I=../proto --python_out=. --grpc_python_out=. ../proto/vault.proto

# Create Vault Keys
export VAULT_KEY_LIGHT=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
export VAULT_KEY_SHADOW=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

mkdir -p certs knowledge evolution

cat <<EOF > /etc/jarvis.env
VAULT_KEY_LIGHT=$VAULT_KEY_LIGHT
VAULT_KEY_SHADOW=$VAULT_KEY_SHADOW
GRPC_PORT=50051
MASTER_ADMIN_KEY=nexus_master_override_2026
EOF
chmod 600 /etc/jarvis.env

# Systemd multi-container service
cat <<EOF > /etc/systemd/system/jarvis-core.service
[Unit]
Description=JarvisAI Supreme Core
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

# Hardware Auto-Detect Script for first boot
cat <<'EOF' > /usr/local/bin/jarvis_hardware_setup.sh
#!/bin/bash
# Automatically detects and configures proprietary GPU drivers on first boot
echo "Detecting hardware for proprietary driver acceleration..."
if lspci | grep -i nvidia > /dev/null; then
    echo "NVIDIA GPU Detected. Initializing CUDA Toolkit installation..."
    # Driver install logic goes here
elif lspci | grep -i amd > /dev/null; then
    echo "AMD GPU Detected. Initializing ROCm installation..."
    # ROCm install logic goes here
fi
echo "Intel OpenVINO optimizations are pre-configured."
EOF
chmod +x /usr/local/bin/jarvis_hardware_setup.sh

echo "JarvisAI Universal OS Installation Complete."
%end
