# Nexus AI Security Suite

**Nexus AI Security Suite** is an advanced, simulated penetration testing and security operations dashboard designed for training, demonstration, and conceptual architectural testing. It provides a highly interactive and visually immersive interface replicating real-world defensive and offensive cyber environments.

**Disclaimer:** This application is entirely simulated. It does not contain actual exploit payloads, nor does it perform real network reconnaissance or unauthorized access. It is designed purely for educational and conceptual demonstration purposes.

## 🚀 Features
- **Cloud Desktop**: An embedded window manager that simulates a remote Kali Linux environment, complete with a functional terminal UI.
- **Jarvis AI Assistant**: A voice-activated AI engine powered by Google Gemini that can interact with the suite, configure simulated exploits, and provide real-time situational awareness.
- **Metasploit Framework UI**: A simulated, high-fidelity replica of the `msfconsole`, seamlessly integrated into the dashboard.
- **Security Recon Lab**: Analyze mock network scans, identify simulated vulnerabilities, and automatically stage mock exploit pipelines.
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
