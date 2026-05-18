import React, { useState, useEffect } from 'react';
import { Monitor, Terminal, X, Minimize2, Maximize2, MonitorOff, ShieldCheck, Wifi, Battery, Clock, Search, Folder, Globe, Command, Key, Plus, Trash2, Loader2, Eye, EyeOff } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { sshKeyService, SSHKey } from '../services/sshKeyService';

export const RemoteDesktop: React.FC = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [securityStatus, setSecurityStatus] = useState<'none' | 'handshaking' | 'verified'>('none');
  const [remoteAddress, setRemoteAddress] = useState('192.168.12.55');
  const [securityToken, setSecurityToken] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);
  const [terminalLogs, setTerminalLogs] = useState<{ text: string, type: 'command' | 'output' | 'error' | 'security' }[]>([
    { text: 'HexStrike Secure Shell v2.5.0 initialized.', type: 'security' },
    { text: 'Local Environment: Secure', type: 'security' }
  ]);
  const [terminalInput, setTerminalInput] = useState('');
  const [showTerminal, setShowTerminal] = useState(true);
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
  const [hsmStatus, setHsmStatus] = useState<{ status: string, serial: string } | null>(null);
  
  // SSH Key Management State
  const [showKeyManager, setShowKeyManager] = useState(false);
  const [sshKeys, setSSHKeys] = useState<SSHKey[]>([]);
  const [selectedKeyId, setSelectedKeyId] = useState<string | null>(null);
  const [isKeysLoading, setIsKeysLoading] = useState(false);
  const [newKeyLabel, setNewKeyLabel] = useState('');
  const [newPublicKey, setNewPublicKey] = useState('');
  const [isAddingKey, setIsAddingKey] = useState(false);
  const [viewingDecryptedKey, setViewingDecryptedKey] = useState<{id: string, text: string} | null>(null);

  useEffect(() => {
    const fetchHSM = async () => {
      try {
        const res = await fetch('/api/security/hsm/status');
        const data = await res.json();
        setHsmStatus(data);
      } catch (e) {
        console.error("HSM offline");
      }
    };
    
    fetchHSM();
    fetchKeys(); // Fetch keys once on mount for the connection screen

    const interval = setInterval(() => {
      setCurrentTime(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
    }, 60000);
    return () => clearInterval(interval);
  }, []);

  const fetchKeys = async () => {
    setIsKeysLoading(true);
    try {
      const keys = await sshKeyService.getKeys();
      setSSHKeys(keys);
    } catch (e) {
      console.error("Failed to fetch keys");
    } finally {
      setIsKeysLoading(false);
    }
  };

  useEffect(() => {
    if (showKeyManager) {
      fetchKeys();
    }
  }, [showKeyManager]);

  const handleAddKey = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newKeyLabel || !newPublicKey) return;
    setIsAddingKey(true);
    try {
      await sshKeyService.addKey(newKeyLabel, newPublicKey);
      setNewKeyLabel('');
      setNewPublicKey('');
      await fetchKeys();
    } catch (e) {
      setValidationError('SSH_KEY_STORAGE_ENCRYPTION_FAILED');
    } finally {
      setIsAddingKey(false);
    }
  };

  const handleDeleteKey = async (id: string) => {
    try {
      await sshKeyService.deleteKey(id);
      await fetchKeys();
    } catch (e) {
      console.error("Delete failed");
    }
  };

  const handleTranslateKey = async (key: SSHKey) => {
    if (viewingDecryptedKey?.id === key.id) {
      setViewingDecryptedKey(null);
      return;
    }
    try {
      const decrypted = await sshKeyService.decryptKey(key.encryptedKey);
      setViewingDecryptedKey({ id: key.id, text: decrypted });
      setTerminalLogs(prev => [...prev, { text: `HSM_DECRYPT_EVENT: User accessed plain-text for identity ${key.label}`, type: 'security' }]);
    } catch (e) {
      console.error("HSM decryption failed");
    }
  };

  // Security Helper: Output Encoding / Sanitization
  const encodeOutput = (text: string) => {
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  };

  const validateInputs = () => {
    // Regex for IP validation
    const ipRegex = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
    if (!ipRegex.test(remoteAddress)) {
      setValidationError('INVALID_REMOTE_IP_FORMAT');
      return false;
    }
    
    // Security Token validation (simulated 8+ chars)
    if (securityToken.length < 8) {
      setValidationError('SECURITY_TOKEN_INSUFFICIENT_ENTROPY');
      return false;
    }

    setValidationError(null);
    return true;
  };

  const handleConnect = async () => {
    if (!validateInputs()) return;

    setIsConnecting(true);
    setSecurityStatus('handshaking');
    
    // 1. Request HSM-backed Session Token (M-TLS Simulation)
    try {
      setTerminalLogs(prev => [...prev, { text: `Contacting HSM (Serial: ${hsmStatus?.serial || '...'})...`, type: 'security' }]);
      
      const selectedKey = sshKeys.find(k => k.id === selectedKeyId);
      const sessionData = {
        target: remoteAddress,
        client: "HEX-CMD-01",
        identity: selectedKey ? selectedKey.label : 'GENERIC_ANONYMOUS',
        identityId: selectedKeyId || 'NULL',
        timestamp: Date.now()
      };

      const hsmRes = await fetch('/api/security/hsm/sign', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ payload: JSON.stringify(sessionData), alias: 'RDP_SIGN_V1' })
      });
      const { signature } = await hsmRes.json();

      setTerminalLogs(prev => [...prev, { text: `HSM_VALID_SIG: ${signature.slice(0, 16)}...`, type: 'security' }]);
      
      // 2. Proof of Possession (PoP) Handshake
      setTimeout(() => {
        setSecurityStatus('verified');
        setTerminalLogs(prev => [...prev, { text: `Handshake established with ${remoteAddress}`, type: 'security' }]);
        setTimeout(() => {
          setIsConnecting(false);
          setIsConnected(true);
        }, 1000);
      }, 1500);

    } catch (err) {
      setValidationError('HSM_COMM_FAILURE_CRYPTO_REQUIRED');
      setIsConnecting(false);
      setSecurityStatus('none');
    }
  };

  const handleTerminalSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!terminalInput.trim()) return;

    // 1. Sanitize and Encode Input (Self-Defense)
    const sanitizedInput = terminalInput.trim();
    setTerminalLogs(prev => [...prev, { text: sanitizedInput, type: 'command' }]);

    // 2. Simulated exploitation check
    if (sanitizedInput.includes('<script>') || sanitizedInput.includes('eval(')) {
      setTerminalLogs(prev => [...prev, { text: 'SECURITY_ALERT: Malicious payload intercepted and encoded.', type: 'error' }]);
      // Show encoding in action
      setTerminalLogs(prev => [...prev, { text: `Encoded Result: ${encodeOutput(sanitizedInput)}`, type: 'security' }]);
    } else {
      // Normal command logic simulation
      setTerminalLogs(prev => [...prev, { text: `Executing: ${sanitizedInput}...`, type: 'output' }]);
    }

    setTerminalInput('');
  };

  if (!isConnected) {
    return (
      <div className="h-[calc(100vh-160px)] bg-slate-950 flex items-center justify-center rounded-lg border border-slate-800 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(6,182,212,0.1)_0%,_transparent_70%)]" />
        
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-slate-900/60 p-8 rounded-3xl border border-slate-800 backdrop-blur-xl text-center space-y-6 w-full max-w-md relative z-10"
        >
          <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-2 border border-slate-700">
             <Monitor className={`w-8 h-8 ${isConnecting ? 'text-cyan-500 animate-pulse' : 'text-slate-500'}`} />
          </div>
          
          <div className="space-y-1">
            <h2 className="text-xl font-bold text-white uppercase italic tracking-tight">SECURE_RDP_GATEWAY</h2>
            <div className="flex items-center justify-center gap-2">
              <p className="text-[9px] text-slate-500 font-mono tracking-widest uppercase">Encryption: AES-256-GCM</p>
              {hsmStatus?.status === 'OPERATIONAL' && (
                <div className="flex items-center gap-1 bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/20">
                  <div className="w-1 h-1 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="text-[8px] text-emerald-500 font-bold tracking-tighter">HSM_FIPS_L3</span>
                </div>
              )}
            </div>
          </div>

          <div className="space-y-4 text-left">
            <div className="space-y-1.5">
               <label className="text-[10px] font-mono text-slate-500 uppercase tracking-widest ml-1">Remote Target Address</label>
               <input 
                 type="text" 
                 value={remoteAddress}
                 onChange={(e) => setRemoteAddress(e.target.value)}
                 disabled={isConnecting}
                 className="w-full bg-black/40 border border-slate-800 rounded-xl px-4 py-3 text-sm text-cyan-500 font-mono focus:border-cyan-500/50 outline-none transition-all"
                 placeholder="0.0.0.0"
               />
            </div>

            <div className="space-y-1.5">
               <label className="text-[10px] font-mono text-slate-500 uppercase tracking-widest ml-1">SSH Identity Key (Vaulted)</label>
               <div className="relative">
                 <select 
                   value={selectedKeyId || ''}
                   onChange={(e) => setSelectedKeyId(e.target.value || null)}
                   disabled={isConnecting}
                   className="w-full bg-black/40 border border-slate-800 rounded-xl px-4 py-3 text-sm text-cyan-500 font-mono focus:border-cyan-500/50 outline-none transition-all appearance-none cursor-pointer pr-10"
                 >
                   <option value="">-- USE_GENERIC_IDENTITY --</option>
                   {sshKeys.map(key => (
                     <option key={key.id} value={key.id}>{key.label.toUpperCase()}</option>
                   ))}
                 </select>
                 <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none">
                   <Key className="w-4 h-4 text-slate-600" />
                 </div>
               </div>
            </div>
            <div className="space-y-1.5">
               <label className="text-[10px] font-mono text-slate-500 uppercase tracking-widest ml-1">Access Token (8+ Characters)</label>
               <div className="relative">
                  <input 
                    type="password" 
                    value={securityToken}
                    onChange={(e) => setSecurityToken(e.target.value)}
                    disabled={isConnecting}
                    className="w-full bg-black/40 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white font-mono focus:border-cyan-500/50 outline-none transition-all"
                    placeholder="••••••••••••"
                  />
                  <div className="absolute right-4 top-1/2 -translate-y-1/2">
                    <ShieldCheck className={`w-4 h-4 ${securityToken.length >= 8 ? 'text-emerald-500' : 'text-slate-700'}`} />
                  </div>
               </div>
            </div>
            
            {validationError && (
              <motion.div 
                initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }}
                className="flex items-center gap-2 text-red-500 text-[10px] font-bold uppercase tracking-tighter bg-red-500/10 p-2 rounded-lg border border-red-500/20"
              >
                <div className="w-1 h-1 rounded-full bg-red-500 animate-ping" />
                {validationError}
              </motion.div>
            )}
          </div>
          
          <div className="flex gap-3">
            <button 
              onClick={() => setShowKeyManager(true)}
              className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all border border-slate-700/50"
            >
              <Key className="w-4 h-4" />
              <span>KEY_VAULT</span>
            </button>

            <button 
              onClick={handleConnect}
              disabled={isConnecting}
              className={`flex-[2] py-4 transition-all flex items-center justify-center gap-3 group disabled:opacity-80 rounded-xl font-bold ${
                securityStatus === 'verified' ? 'bg-emerald-600 text-white' : 'bg-cyan-600 hover:bg-cyan-500 text-white shadow-[0_0_15px_rgba(6,182,212,0.3)]'
              }`}
            >
              {isConnecting ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>{securityStatus === 'handshaking' ? 'M-TLS...' : 'DH_KEY...'}</span>
                </>
              ) : (
                <>
                  <MonitorOff className="w-4 h-4" />
                  <span>ESTABLISH_LINK</span>
                </>
              )}
            </button>
          </div>
          
          <div className="pt-4 flex flex-col items-center justify-center gap-2">
            <div className={`flex items-center gap-2 text-[9px] font-mono uppercase transition-colors ${
              securityStatus === 'verified' ? 'text-emerald-500' : 'text-slate-600'
            }`}>
              <ShieldCheck className="w-3 h-3" />
              <span>{securityStatus === 'verified' ? 'Identity Verified: KALI-X-99' : 'Handshake Protocol: AES-256-GCM'}</span>
            </div>
            {securityStatus === 'handshaking' && (
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: '100%' }}
                className="h-0.5 bg-cyan-500/50 w-32 rounded-full overflow-hidden"
              >
                <motion.div 
                  animate={{ x: [-100, 100] }}
                  transition={{ repeat: Infinity, duration: 1 }}
                  className="h-full w-20 bg-cyan-400"
                />
              </motion.div>
            )}
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-160px)] bg-slate-900 rounded-lg border border-slate-800 flex flex-col relative overflow-hidden shadow-2xl">
      {/* KALI TOP PANEL */}
      <div className="h-7 bg-black border-b border-white/5 flex items-center justify-between px-3 text-white/70 text-[10px] select-none">
        <div className="flex items-center gap-4">
           <div className="flex items-center gap-1.5 hover:text-white transition-colors cursor-pointer">
              <Command className="w-3.5 h-3.5 text-cyan-500" />
              <span className="font-bold">Applications</span>
           </div>
           <div className="flex items-center gap-4 text-white/40">
              <span className="hover:text-white transition-colors cursor-pointer capitalize">Places</span>
              <span className="hover:text-white transition-colors cursor-pointer capitalize">System</span>
           </div>
        </div>
        
        <div className="absolute left-1/2 -translate-x-1/2 font-mono font-medium flex items-center gap-2">
           <Clock className="w-3 h-3 text-cyan-500/50" />
           {currentTime}
        </div>

        <div className="flex items-center gap-4">
           <div className="flex items-center gap-3">
              <Wifi className="w-3.5 h-3.5" />
              <Battery className="w-3.5 h-3.5 text-emerald-500" />
           </div>
           <div className="flex items-center gap-3 border-l border-white/10 pl-3">
              <ShieldCheck className="w-3.5 h-3.5 text-cyan-400" />
              <div className="flex items-center gap-1">
                 <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_5px_rgba(16,185,129,0.5)]" />
                 <span className="font-bold uppercase tracking-tighter">root</span>
              </div>
           </div>
           <button onClick={() => setIsConnected(false)} className="hover:text-red-400 transition-colors">
              <X className="w-4 h-4" />
           </button>
        </div>
      </div>

      {/* DESKTOP AREA */}
      <div className="flex-1 bg-[#1a222c] relative overflow-hidden desktop-canvas">
        {/* BACKGROUND LOGO */}
        <div className="absolute inset-0 flex items-center justify-center opacity-[0.03] pointer-events-none">
           <img src="https://www.kali.org/images/kali-logo.svg" alt="Kali Logo" className="w-1/2 grayscale invert" />
        </div>

        {/* DESKTOP ICONS */}
        <div className="p-4 grid grid-cols-1 w-24 gap-4">
           <DesktopIcon icon={Folder} label="Home" color="text-amber-400" status="connected" />
           <DesktopIcon icon={Search} label="Burp Suite" color="text-orange-500" status="disconnected" />
           <DesktopIcon icon={Terminal} label="Terminal" color="text-slate-300" onClick={() => setShowTerminal(true)} status="connected" />
           <DesktopIcon icon={Globe} label="Browser" color="text-cyan-400" status="connected" />
        </div>

        {/* WINDOWS */}
        <AnimatePresence>
          {showTerminal && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="absolute top-12 left-32 w-2/3 h-2/3 bg-[#0c0c0c] border border-white/10 rounded-lg shadow-2xl flex flex-col backdrop-blur-md"
            >
              {/* Terminal Title Bar */}
              <div className="h-9 bg-[#1a1a1a] border-b border-white/5 flex items-center justify-between px-3 shrink-0 rounded-t-lg">
                <div className="flex items-center gap-3">
                   <Terminal className="w-3.5 h-3.5 text-cyan-500" />
                   <span className="text-[10px] text-white/50 font-mono tracking-tight">root@kali: ~/tools/recon</span>
                </div>
                <div className="flex items-center gap-3">
                   <Minimize2 className="w-3 h-3 text-white/30 cursor-pointer hover:text-white" />
                   <Maximize2 className="w-3 h-3 text-white/30 cursor-pointer hover:text-white" />
                   <X onClick={() => setShowTerminal(false)} className="w-3.5 h-3.5 text-white/30 cursor-pointer hover:text-red-500" />
                </div>
              </div>
              
              {/* Terminal Content */}
              <div className="flex-1 p-4 font-mono text-[11px] overflow-y-auto space-y-1 custom-scrollbar">
                 {terminalLogs.map((log, i) => (
                   <div key={i} className="flex flex-col">
                     {log.type === 'command' && (
                       <div className="flex gap-2">
                         <span className="text-emerald-500">┌──(</span>
                         <span className="text-cyan-400 font-bold">root㉿kali</span>
                         <span className="text-emerald-500">)-[</span>
                         <span className="text-white">~</span>
                         <span className="text-emerald-500">]</span>
                         <div className="flex gap-2">
                           <span className="text-emerald-500">└─#</span>
                           <span className="text-white">{log.text}</span>
                         </div>
                       </div>
                     )}
                     {log.type === 'output' && (
                       <div className="text-slate-400 pl-4 py-0.5 opacity-80 break-all">
                         {log.text}
                       </div>
                     )}
                     {log.type === 'error' && (
                       <div className="text-red-500 pl-4 py-0.5 font-bold animate-pulse uppercase tracking-tighter">
                         {log.text}
                       </div>
                     )}
                     {log.type === 'security' && (
                       <div className="text-cyan-500/60 pl-4 py-0.5 italic border-l border-cyan-500/20 ml-2">
                          [SEC_KERNEL] {log.text}
                       </div>
                     )}
                   </div>
                 ))}
                 
                 <form onSubmit={handleTerminalSubmit} className="flex flex-col gap-1 pt-2">
                    <div className="flex gap-2">
                       <span className="text-emerald-500">┌──(</span>
                       <span className="text-cyan-400 font-bold">root㉿kali</span>
                       <span className="text-emerald-500">)-[</span>
                       <span className="text-white">~</span>
                       <span className="text-emerald-500">]</span>
                    </div>
                    <div className="flex gap-2 items-center">
                       <span className="text-emerald-500">└─#</span>
                       <input 
                         type="text"
                         value={terminalInput}
                         onChange={(e) => setTerminalInput(e.target.value)}
                         className="flex-1 bg-transparent border-none outline-none text-white font-mono"
                         autoFocus
                       />
                       <div className="w-1.5 h-3 bg-cyan-500 animate-pulse" />
                    </div>
                 </form>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* KALI BOTTOM DOCK */}
      <div className="h-12 absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-4 px-6 bg-black/40 border border-white/10 rounded-2xl backdrop-blur-xl shadow-xl">
         <DockIcon icon={Terminal} onClick={() => setShowTerminal(true)} hasIndicator={showTerminal} />
         <DockIcon icon={Folder} />
         <DockIcon icon={Globe} />
         <DockIcon icon={ShieldCheck} />
      </div>

      {/* SSH KEY MANAGER MODAL */}
      <AnimatePresence>
        {showKeyManager && (
          <div className="absolute inset-0 z-[100] flex items-center justify-center p-8">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-black/80 backdrop-blur-sm"
              onClick={() => setShowKeyManager(false)}
            />
            <motion.div 
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="relative w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[80vh]"
            >
              <div className="p-6 border-b border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-cyan-500/10 rounded-lg">
                    <Key className="w-5 h-5 text-cyan-500" />
                  </div>
                  <div>
                    <h3 className="text-white font-bold tracking-tight">SECURE_SSH_VAULT</h3>
                    <p className="text-[10px] text-slate-500 font-mono uppercase tracking-widest">HSM-Backed Key Management</p>
                  </div>
                </div>
                <button 
                  onClick={() => setShowKeyManager(false)}
                  className="p-2 hover:bg-slate-800 rounded-lg text-slate-500 hover:text-white transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-8 custom-scrollbar">
                {/* ADD NEW KEY */}
                <div className="space-y-4">
                  <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                    <Plus className="w-3 h-3" />
                    Register New Identity
                  </h4>
                  <form onSubmit={handleAddKey} className="space-y-3">
                    <input 
                      type="text"
                      placeholder="Identifer (e.g. Kali_Laptop_X1)"
                      value={newKeyLabel}
                      onChange={(e) => setNewKeyLabel(e.target.value)}
                      className="w-full bg-black/40 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white font-mono focus:border-cyan-500/50 outline-none transition-all"
                    />
                    <textarea 
                      placeholder="Paste public key (ssh-rsa ...)"
                      value={newPublicKey}
                      onChange={(e) => setNewPublicKey(e.target.value)}
                      className="w-full bg-black/40 border border-slate-800 rounded-xl px-4 py-3 text-xs text-white/70 font-mono h-24 focus:border-cyan-500/50 outline-none transition-all resize-none"
                    />
                    <button 
                      type="submit"
                      disabled={isAddingKey || !newKeyLabel || !newPublicKey}
                      className="w-full bg-cyan-600 hover:bg-cyan-500 text-white py-3 rounded-xl font-bold text-sm transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                    >
                      {isAddingKey ? <Loader2 className="w-4 h-4 animate-spin" /> : <ShieldCheck className="w-4 h-4" />}
                      ENCRYPT_AND_STORE_IN_VAULT
                    </button>
                  </form>
                </div>

                {/* KEY LIST */}
                <div className="space-y-4">
                  <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Active Keys ({sshKeys.length})</h4>
                  {isKeysLoading ? (
                    <div className="flex justify-center p-8">
                      <Loader2 className="w-6 h-6 text-cyan-500 animate-spin" />
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {sshKeys.length === 0 ? (
                        <div className="text-center py-8 bg-black/20 rounded-2xl border border-dashed border-slate-800 text-slate-600 text-xs italic">
                          No identity keys found in encrypted storage.
                        </div>
                      ) : (
                        <div className="space-y-4">
                          {sshKeys.map(key => (
                            <div key={key.id} className="space-y-1">
                              <div className="group p-4 bg-black/40 border border-slate-800 rounded-2xl flex items-center justify-between hover:border-slate-700 transition-all">
                                <div className="flex items-center gap-4">
                                  <div className="w-10 h-10 bg-slate-800 rounded-xl flex items-center justify-center text-slate-500 group-hover:text-cyan-400 transition-colors">
                                    <Key className="w-5 h-5" />
                                  </div>
                                  <div>
                                    <p className="text-sm font-bold text-white tracking-tight">{key.label}</p>
                                    <p className="text-[9px] text-slate-500 font-mono uppercase tracking-tighter">
                                      ID: {key.id.slice(0, 8)}... // Created: {new Date(key.createdAt).toLocaleDateString()}
                                    </p>
                                  </div>
                                </div>
                                <div className="flex items-center gap-2">
                                  <button 
                                    onClick={() => handleTranslateKey(key)}
                                    className={`p-2 rounded-lg transition-colors ${viewingDecryptedKey?.id === key.id ? 'bg-cyan-500/20 text-cyan-400' : 'hover:bg-slate-800 text-slate-500 hover:text-cyan-400'}`}
                                    title="Translate Key (HSM)"
                                  >
                                    {viewingDecryptedKey?.id === key.id ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                  </button>
                                  <button 
                                    onClick={() => handleDeleteKey(key.id)}
                                    className="p-2 hover:bg-red-500/10 rounded-lg text-slate-500 hover:text-red-500 transition-colors"
                                    title="Revoke Key"
                                  >
                                    <Trash2 className="w-4 h-4" />
                                  </button>
                                </div>
                              </div>
                              
                              <AnimatePresence>
                                {viewingDecryptedKey?.id === key.id && (
                                  <motion.div 
                                    initial={{ opacity: 0, height: 0 }}
                                    animate={{ opacity: 1, height: 'auto' }}
                                    exit={{ opacity: 0, height: 0 }}
                                    className="mx-4 mb-2 p-4 bg-black/60 border-x border-b border-slate-800 rounded-b-xl"
                                  >
                                    <div className="flex items-center gap-2 mb-2">
                                      <div className="w-1 h-1 rounded-full bg-cyan-500 animate-pulse" />
                                      <span className="text-[9px] font-mono text-cyan-500/70 border-b border-cyan-500/20">HSM_OUTPUT_DECRYPTED</span>
                                    </div>
                                    <code className="text-[10px] text-emerald-400 font-mono break-all line-clamp-3 opacity-80">
                                      {viewingDecryptedKey.text}
                                    </code>
                                  </motion.div>
                                )}
                              </AnimatePresence>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>

              <div className="p-4 bg-slate-950/50 border-t border-slate-800 text-center">
                <p className="text-[9px] text-slate-600 font-mono uppercase tracking-[0.2em]">All keys are AES-256 encrypted using System Hardware Security Module</p>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};

const DesktopIcon: React.FC<{ icon: any, label: string, color: string, onClick?: () => void, status?: 'connected' | 'disconnected' }> = ({ icon: Icon, label, color, onClick, status }) => (
  <div onClick={onClick} className="flex flex-col items-center gap-1.5 p-2 rounded-lg hover:bg-white/5 cursor-pointer active:scale-95 transition-all group relative">
     <div className={`p-2 rounded-lg bg-black/20 border border-white/5 shadow-lg group-hover:border-white/20 ${color}`}>
        <Icon className="w-6 h-6" />
     </div>
     {status && (
       <div className={`absolute top-2 right-2 w-2 h-2 rounded-full border border-black ${status === 'connected' ? 'bg-emerald-500' : 'bg-red-500'}`} />
     )}
     <span className="text-[10px] text-white/60 font-medium tracking-tight drop-shadow-md">{label}</span>
  </div>
);

const DockIcon: React.FC<{ icon: any, onClick?: () => void, hasIndicator?: boolean }> = ({ icon: Icon, onClick, hasIndicator }) => (
  <div onClick={onClick} className="flex flex-col items-center gap-1 group cursor-pointer relative pt-1">
     <div className="p-2 rounded-xl bg-slate-800/20 hover:bg-slate-700/40 border border-white/5 hover:border-white/20 transition-all">
        <Icon className="w-5 h-5 text-white/50 group-hover:text-white" />
     </div>
     {hasIndicator && (
       <div className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1 h-1 bg-cyan-500 rounded-full shadow-[0_0_5px_rgba(6,182,212,0.8)]" />
     )}
  </div>
);
