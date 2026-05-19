# NEXUS // AI - Production Deployment Container
FROM kalilinux/kali-rolling

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install core tactical tools and build dependencies
RUN apt-get update && apt-get install -y \
    nmap \
    metasploit-framework \
    sqlmap \
    python3 \
    python3-pip \
    nodejs \
    npm \
    git \
    tor \
    && rm -rf /var/lib/apt/lists/*

# Set operational directory
WORKDIR /opt/nexus-ai

# Copy application source
COPY . .

# Install dependencies and build
RUN npm install
RUN npm run build

# Secure the environment
RUN chmod +x backend/*.py

# Port exposure (C2 Registry & Dashboard)
EXPOSE 9091 3000

# Start neural bootstrap
CMD ["npm", "start"]
