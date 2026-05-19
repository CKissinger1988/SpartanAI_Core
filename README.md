# NEXUS // AI - Sentinel Hub (v3.2.0-PROD)

A high-performance, cryptographically fortified offensive/defensive OS interface engineered for professional security operations. Built with a CNSA-compliant architecture, the platform integrates deep system interaction, autonomous AI-driven automation, and full-spectrum exploit lifecycle management.

## 🚀 Core Tactical Capabilities

- **Command Shell (MAIN_SHELL):** High-throughput terminal interface powered by `node-pty` and `xterm.js`, providing native system execution through a strictly defined, secure bridge.
- **AI Analytics Core (AI_CORE):** Multi-engine neural interface supporting Gemini 1.5 Flash and local **Qwen3-Coder-Next (2026 Gold Standard)**. Optimized for real-time vulnerability analysis, automated payload generation, and autonomous task execution.
- **Jarvis Voice Authority:** Full-spectrum system and hardware command execution via integrated Web Speech API. Jarvis is authorized for root-level orchestration through natural language voice prompts.
- **IoT Discovery (SMART_VECTORS):** Autonomous mDNS/Zeroconf discovery engine for mapping and analyzing local smart home devices and IoT hardware.
- **Exploit Database (EXPLOIT_DB):** CNSA-hardened database of weaponized 2025/2026 exploits. Supports automated global synchronization and custom repository ingestion.
- **Global Orchestration:** Autonomous Command & Control (C2) registration via Tor hidden services for secure, untraceable remote command of any deployment.

## 🛡️ CNSA / NSA-Standard Security Architecture

- **At-Rest OS Encryption (LUKS):** Production deployments utilize **AES-256-XTS** with a **512-bit keysize** and **SHA-512** hashing, compliant with NSA CNSA standards for Top Secret information protection.
- **Authenticated Encryption (AES-256-GCM):** Every secret—including configuration files, local exploit payloads, and C2 metadata—is protected by AES-256 in Galois/Counter Mode (GCM).
- **Hardened Hashing (Argon2id):** All user credentials and master keys are secured with **Argon2id** (1GB Memory, 4 Iterations), the industry gold standard for resistance against specialized ASIC hardware.
- **Anonymity Layer:** Integrated Tor transparent proxying for all traffic and automated MAC address randomization (Macchanger) on every boot.

## 🛠️ Tactical ISO Factory

The project includes an autonomous Kali Linux ISO integration suite, allowing for the generation of hardened, pre-configured tactical environments:
- **Automated Deployment:** Fully automated installation via preseed.cfg, including crypto-partitioning and tactical package selection.
- **Jarvis Kali Monitor:** Real-time background monitoring of Kali Rolling updates and security patches, integrated directly into the Jarvis core.
- **NexusAI Desktop:** Forced minimal X11/Openbox environment, ensuring the NexusAI interface is the primary and only available session.

## 💻 Suggested Hardware Specifications

### 🏆 Prime Commander Tier
*Optimized for local-first intelligence and high-speed cryptographic throughput.*
- **GPU:** NVIDIA RTX 4090 / 5090 (24GB+ VRAM) - *Required for local Qwen3-Coder-Next.*
- **RAM:** 64GB DDR5 (6000MT/s+) - *Required for Argon2id overhead.*
- **CPU:** AMD Ryzen 9 9950X or Intel i9-14900K.
- **Storage:** 2TB NVMe Gen5 SSD.

### 🛡️ Field Operator Tier
- **GPU:** NVIDIA RTX 4070 Ti (12GB+ VRAM).
- **RAM:** 32GB DDR5.
- **Storage:** 1TB NVMe Gen4 SSD.

## 📦 Deployment & Initialization

### Prerequisites
- Node.js (v18+)
- Python 3.9+
- **WSL (Kali Linux)** for Windows-based tactical shells and ISO building.

### Installation
1. **Clone & Install:**
   ```bash
   git clone <repository-url>
   cd ckiss
   npm install
   ```
2. **Autonomous Bootstrap:**
   Launch the application to trigger the self-configuring backend. The system will autonomously initialize databases, generate CNSA security keys, and audit the OS environment.
3. **Build Hardened ISO:**
   ```bash
   ./integrate_kali_automated.sh
   ```

## 🔐 Restricted Access Control
Access requires valid credentials generated during the first bootstrap sequence. Operator keys are saved to `INITIAL_CREDENTIALS.txt` upon the first successful uplink and must be rotated immediately.

## 📜 License
Licensed under ISC. Created for authorized security operations.
