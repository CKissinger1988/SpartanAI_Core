# NEXUS // AI - Sentinel Hub

A production-grade, hardened offensive/defensive OS interface built for deep system integration, AI-driven automation, and exploit lifecycle management. Engineered for professional security operations, utilizing Electron with full Context Isolation and a strictly defined preload bridge.

## 🚀 Core Capabilities

- **Command Shell (MAIN_SHELL):** High-performance terminal powered by `node-pty` and `xterm.js`, providing native system interaction through a secure bridge.
- **AI Analytics (AI_CORE):** Unified interface for Jarvis/Gemini/Qwen3 integration. Supports automated vulnerability analysis, payload generation, and autonomous task execution.
- **Tool Dashboard (TOOL_VAULT):** Operational interface for industry-standard tools (Nmap, Metasploit, SQLMap, etc.) with AI-assisted execution logic.
- **IoT Vectoring (SMART_VECTORS):** Automated discovery and analysis of smart home devices and IoT hardware within the operational network.
- **Exploit Manager (EXPLOIT_DB):** Managed database of CVEs and weaponized exploits. Supports automated synchronization with global intelligence feeds and custom repository ingestion.
- **Real-time Telemetry:** Live system performance monitoring, including CPU/Memory utilization and neural uplink status.
- **Hardened Architecture:** 
  - **Context Isolation:** Prevents unauthorized frontend access to Node.js internals.
  - **Secure Bridge:** Strictly typed IPC communication layer in `app/preload.js`.
  - **Native Performance:** Optimized for real-world offensive/defensive engagement.

## 🛠️ Operational Commands

### AI Integration
Prefix requests in the **AI_CORE** with these keywords for routed execution:
- `jarvis <prompt>`: General intent processing via Jarvis AI.
- `gemini <prompt>`: Deep architectural analysis via Gemini 1.5 Flash.
- `analyze <subject>`: Technical breakdown of files, binaries, or system states.
- `explain <command>`: Detailed risk assessment and documentation of system commands.

### Tactical Tools
In the **TOOL_VAULT**, you can engage:
- **AI Analyze:** Executes a diagnostic on the host security posture.
- **Auto Exploit:** Direct injection of CVE payloads into the operational environment.
- **Scan & Recon:** One-click engagement for pre-configured reconnaissance tools.

### Intelligence Management
- **Global Sync:** Synchronizes local signatures with the latest MSF/CVE disclosures (2025/2026).
- **Ingest Repo:** Imports and parses new exploit signatures from external sources.

## 📦 Deployment & Setup

### Prerequisites
- Node.js (v18+)
- Python 3.9+
- WSL (Kali Linux) for Windows hosts

### Initialization

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ckiss
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

3. **Autonomous Bootstrap:**
   The application features a self-configuring backend. Upon the first launch, it will automatically initialize databases, import signatures, and audit the environment.

4. **Build & Execute:**
   ```bash
   npm run build
   npm start
   ```

## 🔐 Access Control
Access to the **NEXUS // AI** terminal requires valid credentials. 

**First Boot Security:**
To ensure maximum security out-of-the-box, the application no longer ships with static default passwords. Upon the very first successful bootstrap:
1. The system generates unique, high-entropy passwords for both the `ADMIN_CORE` and `OPERATOR_01` accounts.
2. These credentials are saved to a local file named `INITIAL_CREDENTIALS.txt` in the project root.
3. **Requirement:** Retrieve your login keys from this file and rotate them immediately after your first uplink.

*Note: `INITIAL_CREDENTIALS.txt` is automatically excluded from source control to prevent exposure.*

## 📜 License
Licensed under ISC. Built for authorized security operations only.
