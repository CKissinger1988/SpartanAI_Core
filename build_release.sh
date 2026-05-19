#!/bin/bash
# NEXUS // AI - Unified Release Builder
# This script manages binary compilation and custom Kali ISO generation.

set -e

VERSION="3.1.0"
BUILD_ISO=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --iso) BUILD_ISO=true ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

echo "--- NEXUS // AI: OPERATIONAL BUILDER (v${VERSION}) ---"

if [ "$BUILD_ISO" = true ]; then
    echo "[+] Mode: Custom Kali ISO Generation (CNSA Standard)"
    echo "[+] Constructing ISO Factory..."
    docker build -t nexus-iso-factory -f Dockerfile.iso .
    
    echo "[+] Initiating lb build process (This will take 30-60 minutes)..."
    # We run in privileged mode for debootstrap/chroot
    docker run --privileged --rm -v "$(pwd)/release:/opt/nexus-iso-build/output" nexus-iso-factory
    
    echo "[+] ISO Build Complete."
else
    echo "[+] Mode: Production Binary Compilation"
    echo "[+] Constructing hardened environment..."
    docker build -t nexus-ai-builder .

    echo "[+] Extracting production binaries..."
    mkdir -p ./release
    docker run --rm -v "$(pwd)/release:/output" nexus-ai-builder bash -c "cp -r /opt/nexus-ai/dist/* /output/"

    echo "[+] Compressing for tactical deployment..."
    tar -czvf "NEXUS_AI_v${VERSION}_DEPLOYMENT.tar.gz" -C ./release .
    echo "Binary Bundle: NEXUS_AI_v${VERSION}_DEPLOYMENT.tar.gz"
fi

echo "--- OPERATION COMPLETE ---"
