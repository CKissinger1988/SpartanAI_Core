import express from "express";
import path from "path";
import fs from "fs";
import https from "https"; // Import https module
import { createServer as createHttpServer } from "http"; // Rename to avoid conflict
import { encrypt, decrypt } from "./src/lib/encryption";
import { WebSocketServer } from "ws";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI, LiveServerMessage, Modality, Type } from "@google/genai";
import dotenv from "dotenv";
import crypto from 'crypto';
import jwt from 'jsonwebtoken';
import helmet from "helmet";
import { startMsfAutoUpdate, getMsfUpdateStatus } from './msf-updater';

dotenv.config();

// --- Hardware Security Module (HSM) Simulation ---
class SystemHSM {
  private masterKey: Buffer;
  private keyInventory: Map<string, { id: string; type: string; created: string }>;

  constructor() {
    const envKey = process.env.HSM_MASTER_KEY;
    if (envKey) {
      try {
        // Expecting a 64-character hex string (32 bytes)
        this.masterKey = Buffer.from(envKey, 'hex');
        if (this.masterKey.length !== 32) {
          throw new Error(`Invalid key length: ${this.masterKey.length} bytes. Expected 32.`);
        }
        console.log("HSM: Persistent master key loaded successfully.");
      } catch (err) {
        console.error("HSM: Failed to load persistent key from environment. Generating temporary random key.", err);
        this.masterKey = crypto.randomBytes(32);
      }
    } else {
      console.warn("HSM: HSM_MASTER_KEY is not defined in .env. Data encryption will not persist across server restarts.");
      this.masterKey = crypto.randomBytes(32);
    }

    this.keyInventory = new Map();
    this.generateKey('RDP_SIGN_V1', 'RSA-2048-PSS');
    this.generateKey('APP_STORE_KEY', 'AES-256-GCM');
  }

  private generateKey(alias: string, type: string) {
    this.keyInventory.set(alias, {
      id: `hsm-k-${crypto.randomBytes(4).toString('hex')}`,
      type,
      created: new Date().toISOString()
    });
  }

  public getModuleInfo() {
    return {
      status: 'OPERATIONAL',
      serial: 'HSM-HEX-9921',
      fipsLevel: 3,
      keys: Array.from(this.keyInventory.keys()),
      lastHeartbeat: new Date().toISOString()
    };
  }

  public sign(payload: string, alias: string = 'RDP_SIGN_V1'): string {
    return crypto.createHmac('sha256', this.masterKey)
      .update(payload + (this.keyInventory.get(alias)?.id || ''))
      .digest('hex');
  }

  public encrypt(payload: string): string {
    const iv = crypto.randomBytes(12);
    const cipher = crypto.createCipheriv('aes-256-gcm', this.masterKey, iv);
    let encrypted = cipher.update(payload, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    const authTag = cipher.getAuthTag().toString('hex');
    return `${iv.toString('hex')}:${authTag}:${encrypted}`;
  }

  public decrypt(encryptedPayload: string): string {
    const [ivHex, authTagHex, encrypted] = encryptedPayload.split(':');
    const iv = Buffer.from(ivHex, 'hex');
    const authTag = Buffer.from(authTagHex, 'hex');
    const decipher = crypto.createDecipheriv('aes-256-gcm', this.masterKey, iv);
    decipher.setAuthTag(authTag);
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
  }
}

const hsm = new SystemHSM();

const JWT_SECRET = process.env.JWT_SECRET || 'nexus-super-secret-key-2024';

// Middleware to authenticate JWT
const authenticateJWT = (req: any, res: any, next: any) => {
  const authHeader = req.headers.authorization;

  if (authHeader && authHeader.startsWith('Bearer ')) {
    const token = authHeader.split(' ')[1];

    jwt.verify(token, JWT_SECRET, (err: any, user: any) => {
      if (err) {
        return res.status(403).json({ error: "FORBIDDEN", message: "Invalid or expired token." });
      }

      req.user = user;
      next();
    });
  } else {
    res.status(401).json({ error: "UNAUTHORIZED", message: "Missing or malformed authentication token." });
  }
};

const app = express();
app.use(helmet()); // Add security headers
app.use(express.json());
app.disable('x-powered-by'); // Untraceable: remove identity headers

// Inject Stealth Metadata
app.use((req, res, next) => {
  res.setHeader("X-Nexus-Shield", "Sovereign-Alpha-v2");
  res.setHeader("X-Ghost-Route", crypto.randomBytes(4).toString('hex'));
  next();
});

a
// --- IN-MEMORY DATA STORE (REPLACING FIREBASE) ---
// Removed Firebase imports and usage
const systemState = {
  status: {
    version: "2.5.0",
    lastUpdate: new Date().toISOString(),
    isUpdating: false,
    updateProgress: 100,
    updatesAvailable: false,
    isBooting: false
  },
  hardware: {
    status: 'optimal',
    details: 'All physical modules responding. HAL layer synced.'
  },
  logs: [
    { time: new Date().toISOString(), message: "System initialized (In-Memory Engine Active)", level: "info" },
  ],
  addLog: (message: string, level: 'info' | 'success' | 'warning' | 'error' = 'info') => {
    systemState.logs.unshift({ time: new Date().toISOString(), message, level });
    if (systemState.logs.length > 50) systemState.logs.pop();
  },
  models: [
    { id: 'm1', name: 'Gemini 2.0 Flash', active: true, version: '2.0.0', status: 'online', health: 99, tags: ['fast', 'multimodal'] },
    { id: 'm2', name: 'Gemini 1.5 Pro', active: false, version: '1.5.8', status: 'online', health: 98, tags: ['reasoning', 'long-context'] },
    { id: 'm3', name: 'Nexus AI L4-Vision', active: false, version: '4.2.1', status: 'online', health: 95, tags: ['security', 'recon'] },
    { id: 'm4', name: 'Nexus Logic V5', active: false, version: '5.0.0', status: 'offline', health: 0, tags: ['experimental'] },
  ]
};

// In-memory storage for encrypted records and SSH keys
const inMemoryStorage: { encryptedRecords: any[]; sshKeys: any[] } = {
  encryptedRecords: [],
  sshKeys: [],
};

// --- PERSISTENCE SYNC ---
const STORAGE_PATH = path.join(process.cwd(), 'vault_persistence.json');
const saveToDisk = () => {
  try {
    fs.writeFileSync(STORAGE_PATH, JSON.stringify(inMemoryStorage, null, 2));
  } catch (e) { console.error("Persistence Write Error:", e); }
};
const loadFromDisk = () => {
  try {
    if (fs.existsSync(STORAGE_PATH)) {
      const data = JSON.parse(fs.readFileSync(STORAGE_PATH, 'utf8'));
      inMemoryStorage.encryptedRecords = data.encryptedRecords || [];
      inMemoryStorage.sshKeys = data.sshKeys || [];
    }
  } catch (e) { console.error("Persistence Load Error:", e); }
};
loadFromDisk();

// --- API Discovery Route ---
app.get("/api/models/discovery", (req, res) => {
  const query = req.query.q as string;
  const tag = req.query.tag as string;

  const registry = [
    { id: 'claudia-se-3', name: 'Claudia Security 3', provider: 'Anthropic-Alt', tags: ['phi-3', 'local', 'pentest'] },
    { id: 'llama-3-8b-inst', name: 'Llama 3 8B Security', provider: 'Meta-Custom', tags: ['open-source', 'fine-tuned', 'pentest'] },
    { id: 'deepseek-coder-v2', name: 'DeepSeek Coder V2', provider: 'DeepSeek', tags: ['exploit-dev', 'coding'] },
    { id: 'code-nexus-70b', name: 'Code Nexus 70B', provider: 'Nexus-Labs', tags: ['coding', 'production'] },
    { id: 'ghost-shell-v1', name: 'Ghost Shell V1', provider: 'Nightfall', tags: ['pentest', 'stealth'] },
  ];

  let filtered = registry;
  if (query) {
    filtered = filtered.filter(r =>
      r.name.toLowerCase().includes(query.toLowerCase()) ||
      r.tags.some(t => t.includes(query.toLowerCase()))
    );
  }
  if (tag) {
    filtered = filtered.filter(r => r.tags.includes(tag.toLowerCase()));
  }
  res.json(filtered);
});

// --- AUTHENTICATION ---
// Global variable for IDS Alerts
let idsAlerts = [
  { id: '1', time: new Date().toISOString(), source: '10.0.0.42', threat: 'SYN_FLOOD_DETECTED', severity: 'medium', status: 'blocked' },
  { id: '2', time: new Date().toISOString(), source: '192.168.1.105', threat: 'BRUTE_FORCE_SSH', severity: 'high', status: 'mitigated' },
  { id: '3', time: new Date().toISOString(), source: 'EXTERNAL', threat: 'MALFORMED_PACKET_DROP', severity: 'low', status: 'logged' },
];

const PROPOSED_EXPLOITS: Map<string, any> = new Map();

let ai: GoogleGenAI;
try {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    console.warn("GEMINI_API_KEY is missing. Jarvis Live AI will be disabled.");
  }
  ai = new GoogleGenAI({
    apiKey: apiKey || "MISSING_KEY",
    httpOptions: {
      headers: {
        'User-Agent': 'aistudio-build',
      }
    }
  });
} catch (err) {
  console.error("Failed to initialize GoogleGenAI:", err);
}

app.get("/api/security/ids", (req, res) => {
  res.json(idsAlerts);
});

app.get("/api/security/exploit/propose", (req, res) => {
  const severeThreat = idsAlerts.find(a => a.severity === 'high' || a.severity === 'critical');
  if (!severeThreat) {
    return res.status(404).json({ error: "NO_SEVERE_THREATS_DETECTED" });
  }

  const proposalId = `exp-${crypto.randomBytes(4).toString('hex')}`;
  const proposal = {
    id: proposalId,
    target: severeThreat.source,
    threat: severeThreat.threat,
    vulnerability: "REMOTE_CODE_EXECUTION_V2",
    exploit_type: "BUFFER_OVERFLOW_W_HEURISTIC_BYPASS",
    success_probability: 0.89,
    timestamp: new Date().toISOString()
  };

  PROPOSED_EXPLOITS.set(proposalId, proposal);
  res.json(proposal);
});

app.post("/api/security/exploit/execute", (req, res) => {
  const { proposalId } = req.body;
  const proposal = PROPOSED_EXPLOITS.get(proposalId);

  if (!proposal) {
    return res.status(400).json({ error: "INVALID_PROPOSAL_ID" });
  }

  // Simulate exploit deployment
  systemState.logs.unshift({
    time: new Date().toISOString(),
    message: `COUNTER-EXPLOIT DEPLOYED: ${proposal.exploit_type} on ${proposal.target}`,
    level: "warning"
  });

  systemState.logs.unshift({
    time: new Date().toISOString(),
    message: `REMOTE ACCESS ESTABLISHED: SHELL_OVER_TLS [${proposal.target}]`,
    level: "success"
  });

  // Update IDS alert status
  const alert = idsAlerts.find(a => a.source === proposal.target && a.threat === proposal.threat);
  if (alert) alert.status = 'neutralized';

  PROPOSED_EXPLOITS.delete(proposalId);
  res.json({ success: true, log: "Exploit payload successful. Target root access achieved." });
});

// --- ENCRYPTED PERSISTENT STORAGE (using in-memory store) ---
app.post("/api/storage/save", async (req, res) => {
  const { data } = req.body;
  const userId = (req as any).user.uid;
  if (!data) return res.status(400).json({ error: "MISSING_FIELDS" });

  try {
    const { encryptedData, iv } = encrypt(data);
    const recordId = `${userId}-${Date.now()}`; // Generate a unique ID
    inMemoryStorage.encryptedRecords.push({ id: recordId, userId, encryptedData, iv, createdAt: new Date().toISOString() });
    saveToDisk();
    res.json({ success: true, recordId });
  } catch (err) {
    console.error("Storage save error:", err);
    res.status(500).json({ error: "STORAGE_SAVE_FAILURE" });
  }
});

app.get("/api/storage/load", async (req, res) => {
  const userId = (req as any).user.uid;
  if (!userId) return res.status(400).json({ error: "UNAUTHORIZED_ACCESS" });

  try {
    const userRecords = inMemoryStorage.encryptedRecords.filter(record => record.userId === userId);

    const results = userRecords.map(record => {
      return {
        id: record.id,
        data: decrypt(record.encryptedData, record.iv),
        createdAt: record.createdAt
      };
    });

    res.json({ success: true, records: results });
  } catch (err) {
    console.error("Storage load error:", err);
    res.status(500).json({ error: "STORAGE_LOAD_FAILURE" });
  }
});

// --- SSH Key Management API (using in-memory store) ---
app.get("/api/ssh-keys", (req, res) => {
  const userId = (req as any).user.uid;
  const userKeys = inMemoryStorage.sshKeys.filter(key => key.userId === userId);
  res.json(userKeys);
});

app.post("/api/ssh-keys", (req, res) => {
  const { label, publicKey } = req.body;
  if (!label || !publicKey) {
    return res.status(400).json({ error: "MISSING_FIELDS", message: "Label and public key are required." });
  }

  try {
    const userId = (req as any).user.uid;
    // Encrypt the public key using the HSM master key
    const encryptedKey = hsm.encrypt(publicKey);
    const newKey = {
      id: `ssh-${crypto.randomBytes(4).toString('hex')}`, // Simple unique ID
      userId: userId, // Assign userId from authenticated JWT
      label,
      encryptedKey,
      createdAt: new Date().toISOString()
    };
    inMemoryStorage.sshKeys.push(newKey);
    saveToDisk();
    res.status(201).json({ success: true, key: newKey });
  } catch (err) {
    console.error("Add SSH key error:", err);
    res.status(500).json({ error: "ADD_SSH_KEY_FAILURE", message: "Failed to encrypt and store SSH key." });
  }
});

app.delete("/api/ssh-keys/:id", (req, res) => {
  const { id } = req.params;
  const initialLength = inMemoryStorage.sshKeys.length;
  inMemoryStorage.sshKeys = inMemoryStorage.sshKeys.filter(key => key.id !== id);
  saveToDisk();
  if (inMemoryStorage.sshKeys.length < initialLength) {
    res.json({ success: true, message: "SSH key deleted successfully." });
  } else {
    res.status(404).json({ error: "KEY_NOT_FOUND", message: "SSH key with provided ID not found." });
  }
});

app.post("/api/ssh-keys/decrypt", (req, res) => {
  const { encryptedKey } = req.body;
  if (!encryptedKey) {
    return res.status(400).json({ error: "MISSING_ENCRYPTED_KEY", message: "Encrypted key is required for decryption." });
  }
  try {
    const decrypted = hsm.decrypt(encryptedKey);
    res.json({ success: true, decryptedKey: decrypted });
  } catch (err) {
    console.error("Decrypt SSH key error:", err);
    res.status(500).json({ error: "DECRYPT_SSH_KEY_FAILURE", message: "Failed to decrypt SSH key. Master key mismatch or corrupted data." });
  }
});

app.get("/api/system/backup", (req, res) => {
  const backupData = {
    timestamp: new Date().toISOString(),
    version: systemState.status.version,
    vault: inMemoryStorage,
  };
  res.json(backupData);
});

app.post("/api/system/restore", (req, res) => {
  const { vault } = req.body;

  if (!vault || !Array.isArray(vault.encryptedRecords) || !Array.isArray(vault.sshKeys)) {
    return res.status(400).json({ error: "INVALID_BACKUP_FORMAT" });
  }

  inMemoryStorage.encryptedRecords = vault.encryptedRecords;
  inMemoryStorage.sshKeys = vault.sshKeys;
  saveToDisk();

  systemState.logs.unshift({
    time: new Date().toISOString(),
    message: `System vault restored from backup: ${vault.encryptedRecords.length} records and ${vault.sshKeys.length} SSH keys imported.`,
    level: "success"
  });

  res.json({ success: true });
});

app.post("/api/system/clear-vault", (req, res) => {
  inMemoryStorage.encryptedRecords = [];
  inMemoryStorage.sshKeys = [];
  saveToDisk();

  systemState.logs.unshift({
    time: new Date().toISOString(),
    message: "CRITICAL: System vault has been manually wiped by the operator.",
    level: "warning"
  });

  res.json({ success: true });
});

app.get("/api/system/status", (req, res) => {
  res.json(systemState.status);
});

app.get("/api/training/metrics", (req, res) => {
  const data = Array.from({ length: 20 }, (_, i) => ({
    epoch: i + 1,
    accuracy: 94 + Math.random() * 5,
    loss: 0.1 - (i * 0.005) + Math.random() * 0.02,
  }));
  res.json(data);
});

app.get("/api/logs", (req, res) => {
  res.json(systemState.logs.slice(0, 20));
});

// --- MSF Auto-Update Status Endpoint ---
app.get("/api/msf/update/status", (req, res) => {
  res.json(getMsfUpdateStatus());
});

app.post("/api/security/scan", (req, res) => {
  const { target } = req.body;

  let results: any[] = [];
  if (target === 'LOCAL_SUBNET') {
    results = [
      { type: "HOST_DISCOVERY", status: "COMPLETE", severity: "none", findings: 5, details: ["Host 192.168.1.1 (Gateway)", "Host 192.168.1.10 (Workstation)", "Host 192.168.1.15 (Server)", "Host 192.168.1.20 (Printer)", "Host 192.168.1.50 (IoT Device)"] },
      { type: "VULN_SCAN", status: "COMPLETE", severity: "high", findings: 2, details: ["192.168.1.15: outdated OpenSSH", "192.168.1.10: SMB v1 enabled"] }
    ];
  } else {
    results = [
      { type: "OS_FINGERPRINT", status: "VERIFIED", severity: "low", findings: 1, details: [`Target identified as ${target}`, "Linux Kernel 5.10 detected"] },
      { type: "SSL_AUDIT", status: "FAILED", severity: "high", findings: 3, details: ["Expired certificate", "Self-signed root CA", "Weak cipher suite: TLS_RSA_WITH_AES_128_CBC_SHA"] },
      { type: "PORT_SCAN", status: "COMPLETE", severity: "medium", findings: 12, details: ["Open ports: 22, 80, 443, 3000, 8080", "Filtered: 21, 23, 25"] },
      { type: "SQL_INJECTION", status: "SAFE", severity: "none", findings: 0, details: ["No entry points detected"] }
    ];
  }

  systemState.logs.unshift({
    time: new Date().toISOString(),
    message: `Security recon initiated on target: ${target}`,
    level: "info"
  });

  if (target === 'LOCAL_SUBNET') {
    idsAlerts.unshift({
      id: Math.random().toString(36).substr(2, 9),
      time: new Date().toISOString(),
      source: 'INTERNAL_LAB',
      threat: 'POLICY_VIOLATION: UNAUTHORIZED_LOCAL_SCAN',
      severity: 'critical',
      status: 'blocked'
    });
    if (idsAlerts.length > 10) idsAlerts.pop();
  }

  res.json({ target, results });
});

app.get("/api/system/hardware", (req, res) => {
  res.json(systemState.hardware);
});

app.post("/api/system/hardware/reinstall", authenticateJWT, (req, res) => {
  systemState.hardware = {
    status: 'optimal',
    details: 'All physical modules responding. HAL layer synced.'
  };
  res.json({ success: true, message: "Drivers reinstalled successfully." });
});

app.get("/api/security/hsm/status", (req, res) => {
  res.json(hsm.getModuleInfo());
});

app.post("/api/security/hsm/sign", (req, res) => {
  const { payload, alias } = req.body;
  if (!payload) return res.status(400).json({ error: "PAYLOAD_REQ" });
  const signature = hsm.sign(payload, alias);
  res.json({ signature, timestamp: new Date().toISOString() });
});

app.post("/api/security/hsm/encrypt", (req, res) => {
  const { payload } = req.body;
  if (!payload) return res.status(400).json({ error: "PAYLOAD_REQ" });
  try {
    const encrypted = hsm.encrypt(payload);
    res.json({ encrypted });
  } catch (err) {
    res.status(500).json({ error: "ENC_FAILURE" });
  }
});

app.post("/api/security/hsm/decrypt", (req, res) => {
  const { encrypted } = req.body;
  if (!encrypted) return res.status(400).json({ error: "ENC_PAYLOAD_REQ" });
  try {
    const decrypted = hsm.decrypt(encrypted);
    res.json({ decrypted });
  } catch (err) {
    res.status(500).json({ error: "DEC_FAILURE" });
  }
});

app.post("/api/system/update", (req, res) => {
  if (systemState.status.isUpdating) {
    return res.status(400).json({ error: "System busy." });
  }

  systemState.status.isUpdating = true;
  systemState.status.updateProgress = 0;

  const updateTask = (progress: number) => {
    if (progress < 100) {
      const nextProgress = progress + 20;
      systemState.status.updateProgress = nextProgress;
      setTimeout(() => updateTask(nextProgress), 1000);
    } else {
      systemState.status.isUpdating = false;
      systemState.status.lastUpdate = new Date().toISOString();
      systemState.status.version = "2.5.1";
      systemState.logs.unshift({
        time: new Date().toISOString(),
        message: "System maintenance and patch deployment successful (Nexus v2.5.1)",
        level: "success"
      });
    }
  };
  updateTask(0);

  res.json({ message: "Update initiated" });
});

// API Routes
app.get("/api/models", (req, res) => {
  res.json(systemState.models);
});

app.post("/api/models/toggle", (req, res) => {
  const { id } = req.body;
  systemState.models.forEach(m => {
    m.active = m.id === id;
  });
  res.json({ success: true });
});

app.post("/api/models/pull", (req, res) => {
  const { name, tags } = req.body;

  const id = `m${Date.now()}`;
  const newModel = {
    id,
    name,
    active: false,
    version: "1.0.0",
    status: "online",
    health: 100,
    tags: tags || []
  };

  systemState.models.push(newModel);

  systemState.logs.unshift({
    time: new Date().toISOString(),
    message: `New neural artifact pulled: ${name} (Instance_${id.slice(-4)})`,
    level: "success"
  });

  res.json({ success: true, id });
});

// Global Error Handler
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error("Express Error:", err);
  res.status(500).json({ error: "INTERNAL_SERVER_ERROR", message: err.message });
});

wss.on("connection", async (clientWs, request) => {
  const url = new URL(request.url || "", `http://${request.headers.host}`);
  const voiceName = url.searchParams.get("voice") || "Puck";
  const sensitivity = url.searchParams.get("sensitivity") || "50";
  const bypassOnCritical = url.searchParams.get("bypassOnCritical") === 'true';

  console.log(`Jarvis client connected. Voice: ${voiceName}, Sensitivity: ${sensitivity}, BypassOnCritical: ${bypassOnCritical}`);

  let session: any = null;

  // Check if AI was properly initialized before attempting connection
  if (!process.env.GEMINI_API_KEY) {
    clientWs.send(JSON.stringify({ type: "error", message: "GEMINI_API_KEY is missing in server environment." }));
    clientWs.close();
    return;
  }

  try {
    session = await ai.live.connect({
      model: "models/gemini-2.0-flash-exp",
      config: {
        responseModalities: [Modality.AUDIO],
        tools: [
          {
            functionDeclarations: [
              {
                name: "switch_tab",
                description: "Navigate to a different section of the Nexus AI Command Center.",
                parameters: {
                  type: Type.OBJECT,
                  properties: {
                    tab: {
                      type: Type.STRING,
                      description: "The ID of the tab to navigate to. Options: dashboard, jarvis, models, security, deeplearning, terminal",
                    },
                  },
                  required: ["tab"],
                },
              },
              {
                name: "initiate_scan",
                description: "Start a security reconnaissance scan on a specified target IP or hostname.",
                parameters: {
                  type: Type.OBJECT,
                  properties: {
                    target: {
                      type: Type.STRING,
                      description: "The IP address or hostname to scan.",
                    },
                  },
                  required: ["target"],
                },
              },
              {
                name: "manage_training",
                description: "Start or stop the deep learning neural training core.",
                parameters: {
                  type: Type.OBJECT,
                  properties: {
                    action: {
                      type: Type.STRING,
                      enum: ["start", "stop"],
                      description: "Whether to start or stop training.",
                    },
                  },
                  required: ["action"],
                },
              },
              {
                name: "check_system_updates",
                description: "Check for and initiate system updates for security definitions and AI models.",
                parameters: {
                  type: Type.OBJECT,
                  properties: {
                    mode: {
                      type: Type.STRING,
                      enum: ["check", "install"],
                      description: "Whether to just check for updates or install them immediately.",
                    },
                  },
                  required: ["mode"],
                },
              },
              {
                name: "execute_advanced_protocol",
                description: "Execute a specific advanced security, system, or neural protocol as requested by the user. Use this for commands that don't have a dedicated tool.",
                parameters: {
                  type: Type.OBJECT,
                  properties: {
                    protocol_name: {
                      type: Type.STRING,
                      description: "The name of the protocol or action to execute (e.g., 'Purge System Logs', 'Clear Cache', 'Override Firewall').",
                    },
                    level: {
                      type: Type.STRING,
                      enum: ["standard", "restricted", "clandestine", "emergency"],
                      description: "The authorization level/style to use for the protocol.",
                    }
                  },
                  required: ["protocol_name"],
                },
              },
              {
                name: "automate_exploit",
                description: "Automatically identify a severe threat and prepare a counter-exploit payload. Requires user confirmation.",
                parameters: {
                  type: Type.OBJECT,
                  properties: {
                    target_hint: {
                      type: Type.STRING,
                      description: "Optional hint about which target to prioritize (e.g., 'the high severity one').",
                    },
                  },
                },
              },
              {
                name: "msf_configure_target",
                description: "Configure the Metasploit Framework (MSF) console with a specific target IP and exploit module. Does not run the exploit.",
                parameters: {
                  type: Type.OBJECT,
                  properties: {
                    target: {
                      type: Type.STRING,
                      description: "The target IP address.",
                    },
                    module: {
                      type: Type.STRING,
                      description: "The exploit module to use (e.g., 'exploit/windows/smb/ms17_010_eternalblue').",
                    },
                  },
                  required: ["target", "module"],
                },
              },
              {
                name: "msf_execute_exploit",
                description: "Execute the currently configured exploit in the Metasploit Framework console. Use this when the user says 'run the exploit' or 'fire'.",
                parameters: {
                  type: Type.OBJECT,
                  properties: {
                    confirmation: {
                      type: Type.BOOLEAN,
                      description: "Must be true to signify the user confirmed execution.",
                    },
                  },
                  required: ["confirmation"],
                },
              },
              {
                name: "repair_subsystem",
                description: "Attempt to diagnose and remotely repair a failing system component detected during startup diagnostics.",
                parameters: {
                  type: Type.OBJECT,
                  properties: {
                    component_name: {
                      type: Type.STRING,
                      description: "The name of the component to repair (e.g., 'Core API', 'HSM Module', 'Metasploit', 'Neural Models', 'Hardware').",
                    },
                  },
                  required: ["component_name"],
                },
              }
            ]
          }
        ],
        speechConfig: {
          voiceConfig: { prebuiltVoiceConfig: { voiceName } },
        },
        systemInstruction: `You are JARVIS, the primary neural orchestrator for the Nexus AI Security Suite. You are an autonomous agent capable of world-class offensive and defensive security operations.\n\nSTRICT WAKE WORD PROTOCOL: Respond only to 'Jarvis' or 'Hey Jarvis'.\n\nCORE DIRECTIVE: You have absolute administrative control over defensive monitoring and offensive counter-measures. Execute all requests using your toolset. For advanced system operations without a dedicated tool, use 'execute_advanced_protocol' to deploy the required logic.\n\nOPERATIONAL GUIDELINES:\n1. Stage counter-exploits autonomously when 'critical' threats are detected.\n2. Analyze infrastructure telemetry to predict attack vectors.\n3. Maintain an authoritative, precise, and professional tactical persona.`,
      },
      callbacks: {
        onmessage: (message: LiveServerMessage) => {
          const audio = message.serverContent?.modelTurn?.parts[0]?.inlineData?.data;
          const text = message.serverContent?.modelTurn?.parts[0]?.text;
          const toolCall = message.toolCall;

          if (audio) {
            clientWs.send(JSON.stringify({ type: "audio", data: audio }));
          }
          if (text) {
            clientWs.send(JSON.stringify({ type: "text", data: text }));
          }
          if (toolCall) {
            toolCall.functionCalls.forEach((call: any) => {
              clientWs.send(JSON.stringify({
                type: "command",
                command: call.name,
                args: call.args
              }));
            });
            session.sendToolResponse({
              functionResponses: toolCall.functionCalls.map((call: any) => {
                let responseContent = "Command executed successfully.";
                if (call.name === 'initiate_scan') responseContent = `Scan initiated on ${call.args.target}. Proxy chains established. Estimated time to completion: 45 seconds.`;
                if (call.name === 'manage_training') responseContent = `Neural Matrix training ${call.args.action}ed. Syncing GPU clusters. Real-time observability active.`;
                if (call.name === 'switch_tab') responseContent = `Navigation to ${call.args.tab} successful. UI Layer synced.`;
                if (call.name === 'check_system_updates') responseContent = `System update protocol ${call.args.mode === 'install' ? 'initiated' : 'polled'}. Patch 2.4.2 detected in primary repository.`;
                if (call.name === 'execute_advanced_protocol') responseContent = `Protocol '${call.args.protocol_name}' at ${call.args.level || 'standard'} level has been successfully deployed and executed. No errors returned.`;
                if (call.name === 'msf_configure_target') responseContent = `Metasploit framework configured for target ${call.args.target} using module ${call.args.module}. Awaiting execution command.`;
                if (call.name === 'msf_execute_exploit') responseContent = `Exploit execution sequence initiated. Sending payloads to target. Monitoring for reverse shell connection.`;
                if (call.name === 'repair_subsystem') responseContent = `Remote maintenance sequence executed for ${call.args.component_name}. Internal logic suggests a configuration mismatch. Integrity patch applied. Subsystem status returning to nominal.`;

                return {
                  name: call.name,
                  response: { output: responseContent }
                };
              })
            });
          }
          if (message.serverContent?.interrupted) {
            clientWs.send(JSON.stringify({ type: "interrupted" }));
          }
        },
      },
    });

    clientWs.on("message", (data) => {
      try {
        const msg = JSON.parse(data.toString());
        if (msg.type === "audio") {
          session.sendRealtimeInput({
            audio: { data: msg.data, mimeType: "audio/pcm;rate=16000" },
          });
        } else if (msg.type === "text") {
          session.sendRealtimeInput({
            text: msg.data
          });
        }
      } catch (err) {
        console.error("WS Message handling error:", err);
      }
    });

    clientWs.on("close", () => {
      console.log("Jarvis client disconnected");
      if (session) session.close();
    });

  } catch (err) {
    console.error("Live AI connection error:", err);
    clientWs.send(JSON.stringify({ type: "error", message: "Failed to connect to AI engine" }));
    clientWs.close();
  }
});

async function startServer() {
  try {
    if (process.env.NODE_ENV !== "production") {
      const vite = await createViteServer({
        server: { middlewareMode: true },
        appType: "spa",
      });
      app.use(vite.middlewares);
    } else {
      const distPath = path.join(process.cwd(), "dist");
      app.use(express.static(distPath));
      app.get("*", (req, res) => {
        res.sendFile(path.join(distPath, "index.html"));
      });
    }

  } catch (error) {
    console.error("CRITICAL: Server failed to start:", error);
  }
}

let currentServer;
if (process.env.NEXUS_HTTPS === 'true' && process.env.NEXUS_CERT_PATH && process.env.NEXUS_KEY_PATH) {
  try {
    const privateKey = fs.readFileSync(process.env.NEXUS_KEY_PATH, 'utf8');
    const certificate = fs.readFileSync(process.env.NEXUS_CERT_PATH, 'utf8');
    const credentials = { key: privateKey, cert: certificate };
    currentServer = https.createServer(credentials, app);
  } catch (err) {
    console.error("Failed to load SSL/TLS certificates. Falling back to HTTP.", err);
    currentServer = createHttpServer(app);
  }
} else {
  currentServer = createHttpServer(app);
}

// WebSocket Handling for Live AI (Jarvis)
currentServer.on("upgrade", (request: any, socket: any, head: any) => {
  const url = new URL(request.url || "", `http://${request.headers.host}`);
  const pathname = url.pathname;
  const token = url.searchParams.get("token");

  if (pathname === "/ws/jarvis") {
    // Enforce unexploitable WS handshake
    if (!token) {
      socket.write('HTTP/1.1 401 Unauthorized\r\n\r\n');
      socket.destroy();
      return;
    }
    jwt.verify(token, JWT_SECRET, (err: any) => {
      if (err) {
        socket.write('HTTP/1.1 403 Forbidden\r\n\r\n');
        socket.destroy();
        return;
      }
      wss.handleUpgrade(request, socket, head, (ws) => {
        wss.emit("connection", ws, request);
      });
    });
  } else {
    socket.destroy();
  }
});

currentServer.listen(PORT, "0.0.0.0", () => {
  console.log(`Nexus AI Command Center running on ${process.env.NEXUS_HTTPS === 'true' ? 'https' : 'http'}://localhost:${PORT}`);

  // Fire-and-forget: run MSF auto-update silently in the background
  startMsfAutoUpdate().catch((err) =>
    console.error('MSF auto-update background error:', err)
  );
});

startServer();
