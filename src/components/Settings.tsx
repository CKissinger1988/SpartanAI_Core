import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import {
  X, Shield, Brain, Key, Download, Upload, Trash2, Mic
} from 'lucide-react';
import { AudioSettingsPanel } from './AudioSettingsPanel';
import { useAudioSettings } from '../contexts/AudioSettingsContext';

interface SettingsProps {
  open: boolean;
  onClose: () => void;
}

export const Settings: React.FC<SettingsProps> = ({ open, onClose }) => {
  const fileInputRef = React.useRef<HTMLInputElement>(null);
  const { selectedVoice, setSelectedVoice, wakeWordSensitivity, setWakeWordSensitivity, allowWakeWordBypassOnCritical, setAllowWakeWordBypassOnCritical } = useAudioSettings();
  const [stealthMode, setStealthMode] = React.useState(localStorage.getItem('nexus_stealth_mode') === 'true');
  const [secondaryKey, setSecondaryKey] = React.useState(localStorage.getItem('nexus_secondary_key') || 'NEXUS-7742-X');

  const handleStealthToggle = () => {
    const newValue = !stealthMode;
    setStealthMode(newValue);
    localStorage.setItem('nexus_stealth_mode', String(newValue));
    window.dispatchEvent(new CustomEvent('stealth-mode-update', { detail: { enabled: newValue, key: secondaryKey } }));
  };

  const handleKeyChange = (val: string) => {
    setSecondaryKey(val);
    localStorage.setItem('nexus_secondary_key', val);
    window.dispatchEvent(new CustomEvent('stealth-mode-update', { detail: { enabled: stealthMode, key: val } }));
  };

  const handleImportBackup = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const content = e.target?.result as string;
        const backupData = JSON.parse(content);

        const res = await fetch('/api/system/restore', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(backupData)
        });

        if (!res.ok) throw new Error("RESTORE_FAILED");
        window.dispatchEvent(new CustomEvent('system-notification', {
          detail: { message: "SYSTEM_RESTORE: Vault records successfully re-synchronized." }
        }));
        // The system is in-memory; UI will reflect changes on next data poll.
      } catch (err) {
        console.error("Restore failed:", err);
      }
    };
    reader.readAsText(file);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleExportBackup = async () => {
    try {
      const res = await fetch('/api/system/backup');
      if (!res.ok) throw new Error("BACKUP_FETCH_FAILED");

      const data = await res.json();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `nexus_vault_backup_${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Backup export failed:", err);
    }
  };

  const handleClearVault = async () => {
    const confirmed = window.confirm("CRITICAL WARNING: You are about to PERMANENTLY WIPE the encrypted vault. This will delete all stored credentials and records. This action cannot be undone. Proceed?");
    if (!confirmed) return;

    try {
      const res = await fetch('/api/system/clear-vault', { method: 'POST' });
      if (!res.ok) throw new Error("CLEAR_VAULT_FAILED");

      window.dispatchEvent(new CustomEvent('system-notification', {
        detail: { message: "SYSTEM_PURGE: All vault data sectors have been wiped." }
      }));
      // Success feedback could be added here (e.g., a notification)
    } catch (err) {
      console.error("Clear vault failed:", err);
    }
  };

  const handlePreviewVoice = () => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance("This is a voice preview for Jarvis. All systems nominal.");
      utterance.voice = window.speechSynthesis.getVoices().find(voice => voice.name === selectedVoice) || null;
      utterance.rate = 0.9;
      utterance.pitch = 0.8;
      window.speechSynthesis.cancel(); // Stop any ongoing speech
      window.speechSynthesis.speak(utterance);
    }
  };

  if (!open) return null;

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-6"
        >
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="bg-[#0b0e14] border border-cyan-900/50 w-full max-w-lg rounded-2xl overflow-hidden shadow-2xl"
          >
            <div className="p-4 border-b border-cyan-900/30 flex items-center justify-between">
              <h2 className="text-sm font-mono text-cyan-400 tracking-wider font-bold">SYSTEM_CONFIGURATION</h2>
              <button onClick={onClose} className="p-1 hover:bg-slate-800 rounded">
                <X className="w-5 h-5 text-slate-500" />
              </button>
            </div>

            <div className="p-6 space-y-6">
              {/* AI INTEGRATIONS */}
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-slate-300">
                  <Brain className="w-4 h-4 text-cyan-500" />
                  <span className="text-xs font-bold uppercase tracking-tighter">AI Integrations</span>
                </div>
                <div className="bg-black/40 rounded-lg border border-slate-800 divide-y divide-slate-800/50 text-xs font-mono overflow-hidden">
                  <div className="p-3 flex justify-between items-center">
                    <span className="text-slate-500">Gemini</span>
                    <span className="text-emerald-500">CONFIGURED</span>
                  </div>
                  <div className="p-3 flex justify-between items-center">
                    <span className="text-slate-500">Grok</span>
                    <span className="text-amber-500 text-[10px] px-2 py-0.5 border border-amber-500/20 rounded bg-amber-500/10 cursor-pointer hover:bg-amber-500/20 transition-colors">CONNECT</span>
                  </div>
                  <div className="p-3 flex justify-between items-center">
                    <span className="text-slate-500">Antigravity</span>
                    <span className="text-amber-500 text-[10px] px-2 py-0.5 border border-amber-500/20 rounded bg-amber-500/10 cursor-pointer hover:bg-amber-500/20 transition-colors">CONNECT</span>
                  </div>
                  <div className="p-3 flex justify-between items-center">
                    <span className="text-slate-500">Codex</span>
                    <span className="text-amber-500 text-[10px] px-2 py-0.5 border border-amber-500/20 rounded bg-amber-500/10 cursor-pointer hover:bg-amber-500/20 transition-colors">CONNECT</span>
                  </div>
                  <div className="p-3 flex justify-between items-center">
                    <span className="text-slate-500">Copilot</span>
                    <span className="text-amber-500 text-[10px] px-2 py-0.5 border border-amber-500/20 rounded bg-amber-500/10 cursor-pointer hover:bg-amber-500/20 transition-colors">CONNECT</span>
                  </div>
                </div>
              </div>

              {/* JARVIS PERSONALITY */}
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-slate-300">
                  <Mic className="w-4 h-4 text-cyan-500" />
                  <span className="text-xs font-bold uppercase tracking-tighter">Jarvis Personality</span>
                </div>
                <div className="bg-black/40 rounded-lg border border-slate-800 p-3 space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-500 font-mono uppercase">Voice Profile</span>
                    <select
                      value={selectedVoice}
                      onChange={(e) => setSelectedVoice(e.target.value)}
                      className="bg-slate-900 text-cyan-400 border border-slate-700 rounded px-2 py-1 outline-none text-[10px] cursor-pointer font-mono"
                    >
                      <option value="Puck">PUCK (Default)</option>
                      <option value="Charon">CHARON (Deep)</option>
                      <option value="Kore">KORE (Smooth)</option>
                      <option value="Fenrir">FENRIR (Command)</option>
                      <option value="Aoede">AOEDE (Calm)</option>
                    </select>
                  </div>
                  <button
                    onClick={handlePreviewVoice}
                    className="w-full text-cyan-400 text-[10px] px-2 py-1.5 border border-cyan-500/20 rounded bg-cyan-500/10 hover:bg-cyan-500/20 transition-colors flex items-center justify-center gap-1.5 font-bold uppercase tracking-wider"
                  >
                    <Mic className="w-3 h-3" /> Play Preview
                  </button>

                  <div className="pt-2 space-y-2">
                    <div className="flex justify-between items-center px-1">
                      <span className="text-[9px] text-slate-500 font-mono uppercase tracking-widest">Wake Word Sensitivity</span>
                      <span className="text-[10px] text-cyan-500 font-mono font-bold tracking-tighter">{wakeWordSensitivity}%</span>
                    </div>
                    <input
                      type="range"
                      min="1"
                      max="100"
                      value={wakeWordSensitivity}
                      onChange={(e) => setWakeWordSensitivity(parseInt(e.target.value))}
                      className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500 transition-all hover:bg-slate-700"
                    />
                    <div className="flex justify-between text-[7px] text-slate-600 font-mono uppercase tracking-tighter">
                      <span>Conservative</span>
                      <span>Aggressive</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between px-1 pt-2">
                    <div className="space-y-0.5">
                      <span className="text-[9px] text-slate-500 font-mono uppercase tracking-widest">Wake Word Bypass</span>
                      <p className="text-[7px] text-slate-600 font-mono uppercase">Allow responses without wake word on CRITICAL</p>
                    </div>
                    <button
                      onClick={() => setAllowWakeWordBypassOnCritical(!allowWakeWordBypassOnCritical)}
                      className={`w-8 h-4 rounded-full transition-colors relative ${allowWakeWordBypassOnCritical ? 'bg-cyan-500' : 'bg-slate-800'}`}
                    >
                      <motion.div
                        animate={{ x: allowWakeWordBypassOnCritical ? 18 : 2 }}
                        className="absolute top-1 w-2 h-2 bg-white rounded-full shadow-lg"
                      />
                    </button>
                  </div>
                </div>
              </div>

              {/* STEALTH MODE CONFIGURATION */}
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-slate-300">
                  <Shield className="w-4 h-4 text-purple-500" />
                  <span className="text-xs font-bold uppercase tracking-tighter">Stealth Operations</span>
                </div>
                <div className="bg-black/40 rounded-lg border border-slate-800 p-3 space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <span className="text-[10px] text-slate-400 font-mono uppercase tracking-widest">Enable Stealth Mode</span>
                      <p className="text-[8px] text-slate-600 font-mono">Encrypt all terminal I/O with custom secondary key</p>
                    </div>
                    <button
                      onClick={handleStealthToggle}
                      className={`w-10 h-5 rounded-full transition-all relative ${stealthMode ? 'bg-purple-600 shadow-[0_0_10px_rgba(147,51,234,0.5)]' : 'bg-slate-800'}`}
                    >
                      <motion.div
                        animate={{ x: stealthMode ? 22 : 2 }}
                        className="absolute top-1 w-3 h-3 bg-white rounded-full"
                      />
                    </button>
                  </div>

                  {stealthMode && (
                    <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="space-y-2">
                      <label className="text-[9px] text-slate-500 font-mono uppercase tracking-widest">Secondary Encryption Key</label>
                      <input
                        type="text"
                        value={secondaryKey}
                        onChange={(e) => handleKeyChange(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-[10px] text-purple-400 font-mono outline-none focus:border-purple-500 transition-all"
                        placeholder="Enter custom key..."
                      />
                    </motion.div>
                  )}
                </div>
              </div>

              {/* ENCRYPTED STORAGE STATUS */}
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-slate-300">
                  <Key className="w-4 h-4 text-emerald-500" />
                  <span className="text-xs font-bold uppercase tracking-tighter">Encrypted Storage</span>
                </div>
                <div className="bg-black/40 rounded-lg border border-slate-800 divide-y divide-slate-800/50 text-xs font-mono overflow-hidden">
                  <div className="p-3 flex justify-between items-center">
                    <span className="text-slate-500">ENCRYPTION_KEY</span>
                    <span className="text-emerald-500">32-BYTE MASTER KEY SET</span>
                  </div>
                  <div className="p-3 flex justify-between items-center">
                    <span className="text-slate-500">STORAGE_LOCATION</span>
                    <select className="bg-slate-900 text-cyan-400 border border-slate-700 rounded px-2 py-1 outline-none text-[10px] cursor-pointer">
                      <option value="local">LOCAL_ENCLAVE</option>
                      <option value="cloud">CLOUD_VAULT_AWS</option>
                      <option value="hsm">HARDWARE_SECURITY_MODULE</option>
                      <option value="decentralized">DECENTRALIZED_NODE</option>
                    </select>
                  </div>
                  <div className="p-3 flex justify-between items-center">
                    <span className="text-slate-500">SYSTEM_BACKUP</span>
                    <div className="flex gap-2">
                      <button
                        onClick={handleExportBackup}
                        className="text-cyan-400 text-[10px] px-2 py-0.5 border border-cyan-500/20 rounded bg-cyan-500/10 hover:bg-cyan-500/20 transition-colors flex items-center gap-1.5"
                      >
                        <Download className="w-3 h-3" /> EXPORT
                      </button>
                      <button
                        onClick={() => fileInputRef.current?.click()}
                        className="text-emerald-400 text-[10px] px-2 py-0.5 border border-emerald-500/20 rounded bg-emerald-500/10 hover:bg-emerald-500/20 transition-colors flex items-center gap-1.5"
                      >
                        <Upload className="w-3 h-3" /> IMPORT
                      </button>
                    </div>
                  </div>
                  <div className="p-3 flex justify-between items-center">
                    <span className="text-slate-500 italic">PURGE_DATA_SECTOR</span>
                    <button
                      onClick={handleClearVault}
                      className="text-red-400 text-[10px] px-2 py-0.5 border border-red-500/20 rounded bg-red-500/10 hover:bg-red-500/20 transition-colors flex items-center gap-1.5 font-bold"
                    >
                      <Trash2 className="w-3 h-3" /> CLEAR_VAULT
                    </button>
                  </div>
                </div>
                <input type="file" ref={fileInputRef} onChange={handleImportBackup} accept=".json" className="hidden" />
              </div>
            </div>

            {/* Audio Configuration */}
            <AudioSettingsPanel />

          </div>

          <div className="p-4 bg-slate-950 border-t border-cyan-900/30 flex justify-end">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold uppercase tracking-widest rounded transition-colors"
            >
              Close
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
