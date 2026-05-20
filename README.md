# NEXUS // AI - Sentinel Hub (v3.2.0-PROD)

A professional-grade, CNSA-hardened offensive/defensive tactical OS ecosystem. NexusAI integrates deep system orchestration, autonomous AI intelligence, and full-spectrum exploit management into a single, anonymous, and untraceable environment.

## 🚀 Why NexusAI? (Tactical Advantages)

- **Unrivaled Privacy:** Every NexusAI deployment is a digital fortress. From Tor-only routing to automated MAC randomization and non-persistent logging, you operate with a zero-trace footprint.
- **CNSA Compliance:** Unlike standard distributions, NexusAI is engineered to meet the **Commercial National Security Algorithm (CNSA)** standards for Top Secret data protection. Your payloads, credentials, and communications are secured by the most advanced cryptography available.
- **Jarvis: Your AI Operator:** Move beyond terminal commands. Jarvis is a fully authorized root operator capable of executing complex system and hardware tasks through natural language voice prompts and wake-word detection.
- **Automated Lethality:** The integrated Exploit Database (EXPLOIT_DB) and autonomous IoT discovery engine (SMART_VECTORS) allow for rapid environment mapping and automated vulnerability validation.
- **Instant Deployment:** Generate hardened, pre-configured Kali Linux ISOs in minutes. Our "Factory" approach ensures every field machine is identical, secure, and ready for uplink.

## 🛠️ Core Tactical Features

### 🤖 Jarvis AI Command Core
- **Voice Authority:** Root-level execution via Web Speech API with support for "Jarvis" and "Nexus" wake-words.
- **Autonomous Monitoring:** Real-time tracking of OS health, CPU/Memory load, and Kali Rolling security updates.
- **Orchestration:** Natural language translation of tactical intent into shell-level execution.

### 🛡️ Defensive & Cryptographic Layer
- **At-Rest Encryption:** Full-disk LUKS implementation using **AES-256-XTS (512-bit)** with **SHA-512** hashing.
- **Secure Hashing:** **Argon2id** (1GB Memory, 4 Iterations) for all credentials, providing peak resistance against ASIC-based brute force.
- **Authenticated Payloads:** All local exploits and C2 metadata are secured via **AES-256-GCM** with integrated integrity checks.
- **Anonymity Bridge:** Forced Tor transparent proxying and automated hardware identity rotation (Macchanger) on every boot.

### 📡 Global Command & Control (C2)
- **Tor Uplink:** Untraceable C2 registration via `.onion` hidden services.
- **Secure Bridge:** Cryptographically validated IPC bridge between the Electron frontend and the root-level Python backend.
- **Hardware Integration:** Deep integration with `systeminformation` and native device drivers for hardware-level telemetry.

### 💿 Tactical ISO Factory
- **Automated Preseed:** Zero-touch installation logic that handles everything from crypto-partitioning to tactical package selection.
- **Forced Desktop:** Minimal X11/Openbox environment that locks the OS to the NexusAI interface—preventing unauthorized standard session access.
- **Full Tooling:** Includes the complete `kali-linux-everything` metapackage, ensuring every dependency and tactical tool is present.

## 📦 Deployment & Execution

### 1. Build the Tactical ISO
Generate your hardened deployment image directly from the factory script:
```bash
wsl -d kali-linux -u root -- ./integrate_kali_automated.sh
```

### 2. Autonomous Initialization
Launch the system to trigger the self-configuring backend. The system will autonomously initialize databases, generate CNSA security keys, and establish the Tor uplink.
```bash
npm install
npm run build
npm start
```

## 📱 Future Roadmap: Mobile Integration
Development has commenced on porting the NexusAI ecosystem to Android:
- **Termux Integration:** Headless tactical backend for mobile hardware.
- **Flutter Native Hub:** High-performance mobile UI for remote C2 management and local sensor analysis.

## 🔐 Restricted Access Control
Access requires valid credentials generated during the first bootstrap sequence. Operator keys are saved to `INITIAL_CREDENTIALS.txt` upon the first successful uplink and must be rotated immediately.

## 📜 License
Licensed under ISC. Created for authorized security operations.
