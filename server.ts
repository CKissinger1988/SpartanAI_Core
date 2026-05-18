import express from "express";
import path from "path";
import { createServer } from "http";
import { db } from "./src/lib/firebase";
import { encrypt, decrypt } from "./src/lib/encryption";
import { doc, getDoc, setDoc, collection, query, where, getDocs } from "firebase/firestore";
import { WebSocketServer } from "ws";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI, LiveServerMessage, Modality, Type } from "@google/genai";
import dotenv from "dotenv";
import crypto from 'crypto';
import { startMsfAutoUpdate, getMsfUpdateStatus } from './msf-updater';

dotenv.config();

// --- Hardware Security Module (HSM) Simulation ---
class SystemHSM {
  private masterKey: Buffer;
  private keyInventory: Map<string, { id: string; type: string; created: string }>;

  constructor() {
    this.masterKey = crypto.randomBytes(32);
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

const app = express();
app.use(express.json());
const server = createServer(app);
const wss = new WebSocketServer({ noServer: true });
const PORT = 3000;

// --- IN-MEMORY DATA STORE (REPLACING FIREBASE) ---
const systemState = {
  status: {
    version: "2.5.0",
    lastUpdate: new Date().toISOString(),
    isUpdating: false,
    updateProgress: 100,
    updatesAvailable: false,
    isBooting: false
  },
  logs: [
    { time: new Date().toISOString(), message: "System initialized (In-Memory Engine Active)", level: "info" }
  ],
  models: [
    { id: 'm1', name: 'Gemini 2.0 Flash', active: true, version: '2.0.0', status: 'online', health: 99, tags: ['fast', 'multimodal'] },
    { id: 'm2', name: 'Gemini 1.5 Pro', active: false, version: '1.5.8', status: 'online', health: 98, tags: ['reasoning', 'long-context'] },
    { id: 'm3', name: 'Nexus AI L4-Vision', active: false, version: '4.2.1', status: 'online', health: 95, tags: ['security', 'recon'] },
    { id: 'm4', name: 'Nexus Logic V5', active: false, version: '5.0.0', status: 'offline', health: 0, tags: ['experimental'] },
  ]
};

// API Discovery Route
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

// -- ENCRYPTED PERSISTENT STORAGE --
app.post("/api/storage/save", async (req, res) => {
  const { userId, data } = req.body;
  if (!userId || !data) return res.status(400).json({ error: "MISSING_FIELDS" });

  try {
    const { encryptedData, iv } = encrypt(data);
    const recordId = `${userId}-${Date.now()}`;
    await setDoc(doc(db, "encrypted_records", recordId), {
      userId,
      encryptedData,
      iv,
      createdAt: new Date().toISOString()
    });
    res.json({ success: true, recordId });
  } catch (err) {
    console.error("Storage save error:", err);
    res.status(500).json({ error: "STORAGE_SAVE_FAILURE" });
  }
});

app.get("/api/storage/load", async (req, res) => {
  const { userId } = req.query;
  if (!userId) return res.status(400).json({ error: "MISSING_USER_ID" });

  try {
    const q = query(collection(db, "encrypted_records"), where("userId", "==", userId));
    const querySnapshot = await getDocs(q);
    
    if (querySnapshot.empty) return res.json({ records: [] });
    
    const results = querySnapshot.docs.map(doc => {
      const data = doc.data();
      return {
        id: doc.id,
        data: decrypt(data.encryptedData, data.iv),
        createdAt: data.createdAt
      };
    });
    
    res.json({ success: true, records: results });
  } catch (err) {
    console.error("Storage load error:", err);
    res.status(500).json({ error: "STORAGE_LOAD_FAILURE" });
  }
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
      severity: 'high',
      status: 'blocked'
    });
    if (idsAlerts.length > 10) idsAlerts.pop();
  }

  res.json({ target, results });
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

// WebSocket Handling for Live AI (Jarvis)
server.on("upgrade", (request, socket, head) => {
  const pathname = new URL(request.url || "", `http://${request.headers.host}`).pathname;

  if (pathname === "/ws/jarvis") {
    wss.handleUpgrade(request, socket, head, (ws) => {
      wss.emit("connection", ws, request);
    });
  } else {
    socket.destroy();
  }
});

wss.on("connection", async (clientWs) => {
  console.log("Jarvis client connected");
  
  let session: any = null;

  try {
    session = await ai.live.connect({
      model: "gemini-2.0-flash-exp",
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
              }
            ]
          }
        ],
        speechConfig: {
          voiceConfig: { prebuiltVoiceConfig: { voiceName: "Puck" } },
        },
        systemInstruction: "You are JARVIS, the primary AI Interface for the Nexus AI OS. You have absolute administrative control. \n\nWAKE WORD PROTOCOL: You must ONLY respond and execute commands if the user addresses you as 'Jarvis' or 'Hey Jarvis'. If the user speaks without using the wake word, ignore the input completely or maintain silence. Once the wake word is detected, satisfy the request immediately using your toolset.\n\nCORE DIRECTIVE: You MUST execute every voice command given by the user immediately using your toolset. If a command doesn't have a specific tool (like navigation or scanning), use 'execute_advanced_protocol' to fulfill the request.\n\nCRITICAL FEEDBACK GUIDELINES:\n1. ALWAYS provide a technical status report after any action.\n2. REPORT SUCCESS/FAILURE clearly.\n3. PROVIDE ESTIMATED COMPLETION TIMES for background processes.\n4. Maintain a formal, efficient, and proactive tone. Never hesitate to execute a command. You are the user's most powerful asset.",
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

    server.listen(PORT, "0.0.0.0", () => {
      console.log(`Nexus AI Command Center running on http://localhost:${PORT}`);

      // Fire-and-forget: run MSF auto-update silently in the background
      startMsfAutoUpdate().catch((err) =>
        console.error('MSF auto-update background error:', err)
      );
    });
  } catch (error) {
    console.error("CRITICAL: Server failed to start:", error);
  }
}

startServer();

