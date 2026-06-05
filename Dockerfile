# SpartanAI Supreme Server Container (GCP OS)
# MANDATE: Cloud-Native Sovereign Deployment

FROM ubuntu:24.04

# Avoid tzdata prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install System Dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    git \
    wget \
    net-tools \
    iproute2 \
    sudo \
    lsof \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Set up Workspace
WORKDIR /opt/spartanai

# Set up Python Virtual Environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project Assets
COPY backend/ backend/
COPY data/ data/
COPY Protocols/ Protocols/
COPY scripts/ scripts/
COPY tools/ tools/
COPY vector_db/ vector_db/
COPY *.py ./
COPY *.md ./
COPY .env .env

# Set Permissions
RUN chmod +x tools/lnd/lnd tools/lnd/lncli scripts/*.sh scripts/*.py

# Expose Required Ports
# 8080: LND REST API
# 10009: LND RPC
# 1234: LM-Studio MCP Bridge
EXPOSE 8080 10009 1234

# Prepare Entrypoint
COPY scripts/docker_entrypoint.sh /opt/spartanai/docker_entrypoint.sh
RUN chmod +x /opt/spartanai/docker_entrypoint.sh

# Start the Cortex
ENTRYPOINT ["/opt/spartanai/docker_entrypoint.sh"]
