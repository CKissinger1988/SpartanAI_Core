import React, { useEffect, useState, useCallback, useRef } from 'react';
import { Monitor, ExternalLink, Terminal, RefreshCw, CheckCircle, Radio, ShieldCheck, Activity, Shield, Cpu, Lock } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { IDSAlerts } from './IDSAlerts';
import { NeuralFirewall } from './NeuralFirewall';
import { RemoteADB } from './RemoteADB';
import { useAuth } from '../contexts/AuthContext';

interface DashboardProps {
  onLaunchDesktop?: () => void;
  systemCheck?: {
    inProgress: boolean;
    progress: number;
    currentStep: string;
    results: { name: string; status: 'online' | 'offline' | 'error' | 'pending' }[];
  };
}

const StatusGauge = ({ label, value, max = 100, colorClass = 'text-cyan-500' }: { label: string, value: number, max?: number, colorClass?: string }) => {
  const radius = 32;
  const stroke = 4;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (value / max) * circumference;

  return (
    <div className="flex flex-col items-center justify-center p-4 bg-slate-900/20 border border-slate-800 rounded-xl relative overflow-hidden glow-pulse-edge w-full text-center">
      <svg height={radius * 2} width={radius * 2} className="transform -rotate-90">
        <circle
          stroke="rgba(255,255,255,0.03)"
          fill="transparent"
          strokeWidth={stroke}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <motion.circle
          className={colorClass}
          stroke="currentColor"
          fill="transparent"
          strokeWidth={stroke}
          strokeDasharray={circumference + ' ' + circumference}
          style={{ strokeDashoffset }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
      </svg>
      <div className="absolute top-[32px] flex flex-col items-center justify-center">
        <span className="text-[11px] font-black font-mono text-white tracking-tighter">{value}%</span>
      </div>
      <span className="text-[8px] font-mono text-slate-500 uppercase tracking-widest mt-3 font-bold">{label}</span>
    </div>
  );
};

export const Dashboard: React.FC<DashboardProps> = ({ onLaunchDesktop, systemCheck }) => {
  const { authenticatedFetch } = useAuth();
  const [systemStatus, setSystemStatus] = useState<any>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [c2Status, setC2Status] = useState<any>(null);

  // Holographic Hub States
  const [stealthActive, setStealthActive] = useState(false);
  const [decoyActive, setDecoyActive] = useState(false);
  const [counterActive, setCounterActive] = useState(false);
  const [enclaveLocked, setEnclaveLocked] = useState(true);

  // Fluctuating Gauge States
  const [shieldVal, setShieldVal] = useState(98);
  const [entropyVal, setEntropyVal] = useState(24);
  const [threatIndex, setThreatIndex] = useState(12);

  // Terminal States
  const [terminalInput, setTerminalInput] = useState('');
  const [terminalLogs, setTerminalLogs] = useState<string[]>([
    'NEXUS_SHELL v2.5.0-STABLE READY.',
    'ENTER SYSTEM COMMAND: status, probe network, sync hsm, purge vault'
  ]);
  const consoleBottomRef = useRef<HTMLDivElement>(null);

  const fetchSystemData = useCallback(async () => {
    try {
      const [statusRes, logsRes] = await Promise.all([
        authenticatedFetch('/api/system/status'),
        authenticatedFetch('/api/logs')
      ]);

      if (statusRes.ok) {
        const status = await statusRes.json();
        setSystemStatus(status);
        // Map threat levels to Threat Index
        if (status.threatLevel === 'critical') setThreatIndex(94);
        else if (status.threatLevel === 'high') setThreatIndex(78);
        else if (status.threatLevel === 'medium') setThreatIndex(46);
        else setThreatIndex(15);
      }
      if (logsRes.ok) setLogs(await logsRes.json());

      const c2Res = await authenticatedFetch('/api/c2/mobile/status');
      if (c2Res.ok) {
        setC2Status(await c2Res.json());
      }
    } catch (err) {
      console.error("Fetch failed", err);
    }
  }, [authenticatedFetch]);

  useEffect(() => {
    fetchSystemData();
    const interval = setInterval(fetchSystemData, 3000);
    return () => clearInterval(interval);
  }, [fetchSystemData]);

  // Fluctuations for visual realism
  useEffect(() => {
    const timer = setInterval(() => {
      setShieldVal(prev => Math.max(95, Math.min(100, prev + (Math.random() > 0.5 ? 1 : -1))));
      setEntropyVal(prev => Math.max(15, Math.min(45, prev + Math.floor(Math.random() * 5 - 2))));
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  // Scroll terminal logs to bottom
  useEffect(() => {
    if (consoleBottomRef.current) {
      consoleBottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [terminalLogs]);

  const initiateUpdate = async () => {
    try {
      await authenticatedFetch('/api/system/update', { method: 'POST' });
    } catch (err) {
      console.error("Failed to initiate update");
    }
  };

  const handleCommandSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!terminalInput.trim()) return;

    const cmd = terminalInput.trim().toLowerCase();
    setTerminalLogs(prev => [...prev, `operator@nexusai:~$ ${terminalInput}`]);
    setTerminalInput('');

    try {
      const res = await authenticatedFetch('/api/security/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: cmd })
      });
      const data = await res.json();
      if (res.ok) {
        setTerminalLogs(prev => [...prev, ...data.output]);
      } else {
        setTerminalLogs(prev => [...prev, `ERROR: ${data.error || 'Execution failed'}`]);
      }
    } catch (err) {
      setTerminalLogs(prev => [...prev, 'ERROR: Host communication failure.']);
    }
  };

  const hasSystemError = systemCheck?.results.some(r => r.status === 'offline' || r.status === 'error');

  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      {/* Header Info */}
      <div className="flex justify-between items-end">
        <div className="flex flex-col gap-1">
          <h2 className="text-xl font-bold tracking-tight text-white uppercase italic">SYSTEM_STATUS_REPORT</h2>
          <p className="text-[10px] text-slate-500 font-mono tracking-widest uppercase">
            Nexus Security Suite v{systemStatus?.version || '2.5.0'} // ENVIRONMENT: PRODUCTION
          </p>
        </div>

        <button
          onClick={initiateUpdate}
          disabled={systemStatus?.isUpdating}
          className={`px-4 py-1.5 rounded border flex items-center gap-2 transition-all ${systemStatus?.isUpdating
            ? 'bg-cyan-500/10 border-cyan-500/40 text-cyan-500 cursor-wait'
            : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:border-slate-600 hover:text-slate-200'
            }`}
        >
          {systemStatus?.isUpdating ? (
            <>
              <RefreshCw className="w-3 h-3 animate-spin" />
              <span className="text-[9px] font-mono uppercase tracking-[0.2em]">Maintenance_{systemStatus?.updateProgress}%</span>
            </>
          ) : (
            <>
              <RefreshCw className="w-3 h-3" />
              <span className="text-[9px] font-mono uppercase tracking-[0.2em]">System_Maintenance</span>
            </>
          )}
        </button>
      </div>

      {systemStatus?.isUpdating && (
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="space-y-2 animate-in fade-in duration-300">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse shadow-[0_0_8px_rgba(6,182,212,0.5)]"></div>
            <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-widest">Patching system core & AI definitions...</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="h-1 flex-1 bg-slate-800 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-cyan-500"
                animate={{ width: `${systemStatus.updateProgress}%` }}
              />
            </div>
            <span className="text-[9px] font-mono text-cyan-600 shrink-0">EST_REMAINING: {(10 - (systemStatus.updateProgress / 10))}s</span>
          </div>
        </motion.div>
      )}

      {systemCheck?.inProgress && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{
            opacity: 1,
            height: 'auto',
            borderColor: hasSystemError ? ['#ef4444', 'rgba(239, 68, 68, 0.3)', '#ef4444'] : 'rgba(6, 182, 212, 0.2)',
          }}
          transition={{
            borderColor: hasSystemError ? { duration: 2, repeat: Infinity, ease: "easeInOut" } : { duration: 0.3 },
            height: { duration: 0.3 }
          }}
          className="p-6 bg-cyan-950/10 border rounded-2xl space-y-4 glow-pulse-edge"
        >
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <RefreshCw className="w-4 h-4 text-cyan-500 animate-spin" />
              <h3 className="text-xs font-bold text-white uppercase tracking-[0.2em]">Initial System Diagnostics</h3>
            </div>
            <span className="text-[10px] font-mono text-cyan-500 font-bold">{systemCheck?.progress}%</span>
          </div>

          <div className="h-1.5 w-full bg-slate-900 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.5)]"
              animate={{ width: `${systemCheck?.progress}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {systemCheck.results.map((res, i) => (
              <div key={i} className="flex items-center gap-2 bg-black/40 p-2 rounded-lg border border-white/5">
                <div className={`w-1.5 h-1.5 rounded-full ${res.status === 'online' ? 'bg-emerald-500 shadow-[0_0_5px_rgba(16,185,129,0.5)]' :
                  res.status === 'offline' ? 'bg-red-500 shadow-[0_0_5px_rgba(239,68,68,0.5)]' :
                    res.status === 'error' ? 'bg-amber-500 shadow-[0_0_5px_rgba(245,158,11,0.5)]' :
                      'bg-slate-700'
                  }`} />
                <span className="text-[9px] font-mono text-slate-400 uppercase tracking-tighter">{res.name}</span>
              </div>
            ))}
          </div>
          <p className="text-[9px] font-mono text-slate-500 italic text-center uppercase tracking-widest">{systemCheck?.currentStep}</p>
        </motion.div>
      )}

      {/* Dynamic Status Gauges */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatusGauge label="Shield Integrity" value={shieldVal} colorClass="text-emerald-500" />
        <StatusGauge label="Threat Index" value={threatIndex} max={100} colorClass="text-red-500" />
        <StatusGauge label="Network Entropy" value={entropyVal} colorClass="text-cyan-500" />
      </div>

      {/* Main Grid Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* Cloud Desk */}
          <div
            onClick={onLaunchDesktop}
            className="group relative h-40 immersive-card bg-[#0a0f18]/30 flex flex-col justify-between overflow-hidden cursor-pointer glow-pulse-edge"
          >
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_rgba(6,182,212,0.05)_0%,_transparent_70%)]" />

            <div className="relative p-6 flex flex-col h-full justify-between">
              <div className="flex justify-between items-start">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Monitor className="w-4 h-4 text-cyan-500" />
                    <h3 className="font-black text-md text-white tracking-tighter italic">LAUNCH_CLOUD_DESK</h3>
                  </div>
                  <p className="text-[9px] text-slate-500 font-mono tracking-[0.2em] uppercase">KALI_LINUX_QT6_INSTANCE // SESSION: RDP-01</p>
                </div>
                <div className="p-2 bg-slate-900/80 border border-slate-800 rounded-full text-cyan-500 group-hover:scale-115 group-hover:border-cyan-500/50 transition-all shadow-xl">
                  <ExternalLink className="w-3.5 h-3.5" />
                </div>
              </div>

              <div className="flex gap-10 items-end">
                <div className="space-y-1">
                  <div className="text-[7px] font-mono text-slate-600 uppercase tracking-widest">Protocol</div>
                  <div className="text-[10px] font-bold text-slate-300">RDP / AES-256GCM</div>
                </div>
                <div className="space-y-1">
                  <div className="text-[7px] font-mono text-slate-600 uppercase tracking-widest">Security</div>
                  <div className="text-[10px] font-bold text-emerald-500 uppercase tracking-tighter">Verified End-to-End</div>
                </div>
                <div className="flex-1 text-right">
                  <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 bg-cyan-500/10 border border-cyan-500/20 rounded-full text-[8px] font-bold text-cyan-400 tracking-widest uppercase">
                    Tunnel Secured
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Holographic Security Hub & Interactive Terminal */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Holographic Control Hub */}
            <div className="immersive-card p-6 bg-slate-900/10 flex flex-col justify-between glow-pulse-edge min-h-[300px]">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-cyan-500 theme-text" />
                  Holographic Control Hub
                </h3>
                <span className="text-[8px] font-mono text-cyan-500/70 uppercase">Autopilot Active</span>
              </div>

              <div className="space-y-4 my-2 flex-1 flex flex-col justify-center">
                <div className="flex items-center justify-between p-2 bg-black/30 border border-slate-800 rounded-lg hover:border-cyan-500/30 transition-all">
                  <div className="flex flex-col">
                    <span className="text-[9px] font-bold text-slate-200 font-mono">Stealth Evasion</span>
                    <span className="text-[7px] text-slate-500">svchost.exe Masquerade</span>
                  </div>
                  <button
                    onClick={() => setStealthActive(!stealthActive)}
                    className={`relative w-8 h-4 rounded-full transition-all duration-300 ${stealthActive ? 'bg-cyan-600' : 'bg-slate-800'}`}
                  >
                    <motion.div
                      animate={{ x: stealthActive ? 18 : 2 }}
                      className="absolute top-1 w-2 h-2 bg-white rounded-full shadow-lg"
                    />
                  </button>
                </div>

                <div className="flex items-center justify-between p-2 bg-black/30 border border-slate-800 rounded-lg hover:border-cyan-500/30 transition-all">
                  <div className="flex flex-col">
                    <span className="text-[9px] font-bold text-slate-200 font-mono">Decoy HoneyGrid</span>
                    <span className="text-[7px] text-slate-500">Virtual Honeypot Array</span>
                  </div>
                  <button
                    onClick={() => setDecoyActive(!decoyActive)}
                    className={`relative w-8 h-4 rounded-full transition-all duration-300 ${decoyActive ? 'bg-cyan-600' : 'bg-slate-800'}`}
                  >
                    <motion.div
                      animate={{ x: decoyActive ? 18 : 2 }}
                      className="absolute top-1 w-2 h-2 bg-white rounded-full shadow-lg"
                    />
                  </button>
                </div>

                <div className="flex items-center justify-between p-2 bg-black/30 border border-slate-800 rounded-lg hover:border-cyan-500/30 transition-all">
                  <div className="flex flex-col">
                    <span className="text-[9px] font-bold text-slate-200 font-mono">Auto-Countermeasures</span>
                    <span className="text-[7px] text-slate-500">Intrusion Retaliation</span>
                  </div>
                  <button
                    onClick={() => setCounterActive(!counterActive)}
                    className={`relative w-8 h-4 rounded-full transition-all duration-300 ${counterActive ? 'bg-cyan-600' : 'bg-slate-800'}`}
                  >
                    <motion.div
                      animate={{ x: counterActive ? 18 : 2 }}
                      className="absolute top-1 w-2 h-2 bg-white rounded-full shadow-lg"
                    />
                  </button>
                </div>

                <div className="flex items-center justify-between p-2 bg-black/30 border border-slate-800 rounded-lg hover:border-cyan-500/30 transition-all">
                  <div className="flex flex-col">
                    <span className="text-[9px] font-bold text-slate-200 font-mono">Enclave Hardening</span>
                    <span className="text-[7px] text-slate-500">AES-GCM Rest Vault</span>
                  </div>
                  <button
                    onClick={() => setEnclaveLocked(!enclaveLocked)}
                    className={`relative w-8 h-4 rounded-full transition-all duration-300 ${enclaveLocked ? 'bg-cyan-600' : 'bg-slate-800'}`}
                  >
                    <motion.div
                      animate={{ x: enclaveLocked ? 18 : 2 }}
                      className="absolute top-1 w-2 h-2 bg-white rounded-full shadow-lg"
                    />
                  </button>
                </div>
              </div>
            </div>

            {/* Interactive Output Terminal */}
            <div className="immersive-card p-6 bg-slate-900/10 h-[300px] flex flex-col justify-between glow-pulse-edge">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                  <Terminal className="w-4 h-4 text-cyan-500 theme-text" />
                  Nexus Command Shell
                </h3>
                <span className="text-[7px] font-mono text-cyan-500/70">SH_INT_v1.0</span>
              </div>

              <div className="flex-1 space-y-2 font-mono text-[9px] text-slate-400 overflow-y-auto pr-1 my-2 bg-black/60 p-3 rounded-lg border border-slate-800/80 custom-scrollbar">
                {terminalLogs.map((log, i) => (
                  <div key={i} className="leading-tight">
                    <span className={log.startsWith('ERROR:') ? 'text-red-500 font-bold' : log.startsWith('operator') ? 'text-cyan-400 font-bold' : 'text-slate-300'}>
                      {log}
                    </span>
                  </div>
                ))}
                {/* Kernel Logs Sync */}
                {logs.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-slate-800/80 text-slate-500 space-y-1">
                    <div className="text-[7px] tracking-wider text-slate-600 font-bold">KERNEL LOG FEED:</div>
                    {logs.slice(0, 3).map((l, i) => (
                      <div key={i} className="truncate">
                        [{new Date(l.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}] {l.message}
                      </div>
                    ))}
                  </div>
                )}
                <div ref={consoleBottomRef} />
              </div>

              <form onSubmit={handleCommandSubmit} className="flex gap-2 items-center">
                <span className="text-cyan-500 font-bold text-[10px] font-mono">&gt;</span>
                <input
                  type="text"
                  placeholder="Enter system command..."
                  value={terminalInput}
                  onChange={e => setTerminalInput(e.target.value)}
                  className="bg-transparent text-slate-200 font-mono text-[9px] outline-none flex-1 border-none placeholder:text-slate-700"
                />
                <button type="submit" className="hidden" />
              </form>
            </div>
          </div>

          {/* Mobile C2 Sovereign Link */}
          <div className="immersive-card p-6 bg-[#0a0f18]/40 border-slate-800/40 glow-pulse-edge">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <Radio className="w-5 h-5 text-purple-500 animate-pulse" />
                <h3 className="text-sm font-black text-white italic tracking-tighter uppercase">Mobile_C2_Sovereign_Link</h3>
              </div>
              <div className="flex items-center gap-2 px-3 py-1 bg-purple-500/10 border border-purple-500/20 rounded-full text-[9px] font-bold text-purple-400">
                <ShieldCheck className="w-3 h-3" />
                <span>ENCRYPTION: {c2Status?.encryptionLevel || 'AES-XTS'}</span>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-3 bg-black/40 border border-white/5 rounded-xl space-y-1">
                <span className="text-[8px] text-slate-500 uppercase font-mono tracking-widest">Connection</span>
                <p className="text-[10px] text-cyan-400 font-bold font-mono">{c2Status?.connectedNetwork || 'GSM/LTE'}</p>
              </div>
              <div className="p-3 bg-black/40 border border-white/5 rounded-xl space-y-1">
                <span className="text-[8px] text-slate-500 uppercase font-mono tracking-widest">Signal Integrity</span>
                <p className="text-[10px] text-emerald-500 font-bold font-mono">{c2Status?.signalStrength || 0}%</p>
              </div>
              <div className="p-3 bg-black/40 border border-white/5 rounded-xl space-y-1">
                <span className="text-[8px] text-slate-500 uppercase font-mono tracking-widest">C2 Heartbeat</span>
                <p className="text-[10px] text-slate-300 font-bold font-mono">ACTIVE</p>
              </div>
              <div className="p-3 bg-black/40 border border-white/5 rounded-xl space-y-1">
                <span className="text-[8px] text-slate-500 uppercase font-mono tracking-widest">Last Payload</span>
                <p className="text-[10px] text-purple-400 font-bold font-mono">{c2Status?.lastPayloadType || 'IDLE'}</p>
              </div>
            </div>
          </div>

          {/* Neural Firewall */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <NeuralFirewall />
            <div className="immersive-card p-6 bg-[#0a0f18]/40 border-slate-800/40 glow-pulse-edge">
              <RemoteADB />
            </div>
          </div>
        </div>

        {/* IDS Alert Center */}
        <div className="lg:col-span-1">
          <div className="glow-pulse-edge rounded-2xl h-full">
            <IDSAlerts />
          </div>
        </div>
      </div>
    </div>
  );
};