# SentinelAI Security Suite

An advanced, unified AI-powered security operations and threat management suite. SentinelAI provides real-time monitoring, AI-driven threat prediction, and a comprehensive security laboratory environment.

## Features & Capabilities

- **AI-Powered Threat Analysis**: Leverage Google Gemini to analyze network traffic and identify anomalies.
- **Unified Security Dashboard**: Real-time monitoring of system intrusions, scan results, and threat levels.
- **Security Laboratory**: A sandboxed environment for testing vulnerabilities and counter-exploits.
- **Jarvis Voice Interface**: Command and control your security operations through natural language interactions.
- **Real-Time IDS/IPS Simulation**: Monitor and neutralize simulated threats in your perimeter.

## Installation

### Prerequisites

* [Node.js](https://nodejs.org/) (Version 22+ recommended)
* npm (included with Node.js)

### Common Setup

1. **Clone the repository**:
   ```bash
   git clone [YOUR_REPO_URL]
   cd sentinelai-security-suite
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and configure your API keys (specifically `GEMINI_API_KEY`).

### Linux Setup

Follow the Common Setup steps above. Ensure you have `build-essential` installed for any necessary native compilations.

```bash
# Example for Debian/Ubuntu
sudo apt update
sudo apt install build-essential
npm install
npm run dev
```

### Windows Setup

Follow the Common Setup steps above. It is recommended to use Powershell or Git Bash.

1. Ensure Node.js is correctly installed in your PATH.
2. If issues arise with native dependencies, run the terminal as Administrator.
   ```bash
   npm install
   npm run dev
   ```

## Development

- Start development server: `npm run dev`
- Build for production: `npm run build`
- Run production build: `npm run start`

## Technologies

- React 19 / Vite
- Express (Backend API Proxy)
- Tailwind CSS
- Google Gemini API
- Recharts (Data Visualization)
