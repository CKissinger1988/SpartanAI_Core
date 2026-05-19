# Nexus AI Sovereign Security Suite (ASOC)

**Nexus AI Sovereign Security Suite** is a high-performance autonomous security operations center (ASOC) designed for professional offensive and defensive operations. This build is hardened for zero-trace visibility and unexploitable interface boundaries, providing a neural-orchestrated hub for managing distributed infrastructure, hardware-level encryption, and autonomous counter-measures.

## 🚀 Features
- **Operational Enclave**: A zero-trust node management gateway providing secure terminal access and encrypted file operations across distributed assets.
- **Jarvis AI Assistant**: A voice-activated neural orchestrator powered by Gemini 2.0, capable of autonomous infrastructure auditing, threat analysis, and exploit staging.
- **Metasploit Framework Console**: Operational bridge to MSF infrastructure for targeted deployment.
- **Security Recon Lab**: Real-time vulnerability assessment engine and network topology analyzer.
- **Responsive Layout**: Fluid design built with Tailwind CSS, ensuring the dashboard scales from desktop monitors down to mobile devices.

## 🛠️ Installation & Setup

Ensure you have [Node.js](https://nodejs.org/) installed on your machine.

1. **Clone the Repository**
   ```bash
   git clone https://github.com/CKissinger1988/NexusAI-Security-Suite.git
   cd NexusAI-Security-Suite
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Environment Configuration**
   To enable the Jarvis Voice AI features, you must provide a valid Gemini API key. Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Start the Application (Development Mode)**
   This will spin up both the Vite frontend server and the Express backend simultaneously:
   ```bash
   npm run dev
   ```
   The application will be accessible at `http://localhost:5173` (Frontend) and the backend API at `http://localhost:3000`.

## 📦 Building for Production / Releases

To create an optimized production build for deployment:

1. **Build the Application**
   ```bash
   npm run build
   ```
   This will compile the React application and place the static assets into the `dist/` directory.

2. **Run the Production Server**
   ```bash
   npm run start
   ```
   The Express server will serve the optimized frontend files on `http://localhost:3000`. 
   *Note: Ensure your production environment sets the `NODE_ENV=production` environment variable.*

## 📂 Project Structure
- `src/components`: React components including the simulated desktop, terminal, and AI chat interfaces.
- `src/contexts`: React context providers for global state (e.g., AuthContext).
- `server.ts`: Express backend handling simulated security tool endpoints and the WebSocket connection for the Gemini Live API.
- `index.css`: Global styles, including custom animations and the Tailwind configuration.
