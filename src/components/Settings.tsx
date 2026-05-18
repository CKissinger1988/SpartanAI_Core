import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X, Shield, Brain, Key } from 'lucide-react';

interface SettingsProps {
  open: boolean;
  onClose: () => void;
}

export const Settings: React.FC<SettingsProps> = ({ open, onClose }) => {
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
                </div>
              </div>

              {/* GENERAL SETTINGS */}
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-slate-300">
                  <Shield className="w-4 h-4 text-slate-400" />
                  <span className="text-xs font-bold uppercase tracking-tighter">General</span>
                </div>
                <div className="flex justify-between items-center bg-black/40 p-3 rounded-lg border border-slate-800">
                  <span className="text-xs text-slate-400">Simulation Intensity</span>
                  <div className="flex gap-2">
                    <button className="px-2 py-1 text-[10px] bg-cyan-900/30 text-cyan-400 border border-cyan-500/20 rounded">LOW</button>
                    <button className="px-2 py-1 text-[10px] bg-cyan-500 text-black border border-cyan-500 rounded font-bold">MED</button>
                    <button className="px-2 py-1 text-[10px] bg-cyan-900/30 text-cyan-400 border border-cyan-500/20 rounded">HIGH</button>
                  </div>
                </div>
              </div>
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
        </motion.div>
      )}
    </AnimatePresence>
  );
};
