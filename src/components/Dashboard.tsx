import React, { useEffect, useState } from 'react';
import { Monitor, ExternalLink, Terminal, RefreshCw, CheckCircle } from 'lucide-react';
import { motion } from 'motion/react';
import { IDSAlerts } from './IDSAlerts';

export const Dashboard: React.FC<{ onLaunchDesktop?: () => void }> = ({ onLaunchDesktop }) => {
  const [systemStatus, setSystemStatus] = useState<any>(null);
  const [logs, setLogs] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statusRes, logsRes] = await Promise.all([
          fetch('/api/system/status'),
          fetch('/api/logs')
        ]);
        
        if (statusRes.ok) setSystemStatus(await statusRes.json());
        if (logsRes.ok) setLogs(await logsRes.json());
      } catch (err) {
        console.error("Fetch failed", err);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  const initiateUpdate = async () => {
    try {
      await fetch('/api/system/update', { method: 'POST' });
    } catch (err) {
      console.error("Failed to initiate update");
    }
  };


  return (
    <div className="space-y-8 animate-in fade-in duration-700">
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
          className={`px-4 py-1.5 rounded border flex items-center gap-2 transition-all ${
            systemStatus?.isUpdating 
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
        <motion.div 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-3 bg-cyan-950/20 border border-cyan-500/20 rounded-lg flex items-center justify-between"
        >
          <div className="flex items-center gap-3">
             <div className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse shadow-[0_0_8px_rgba(6,182,212,0.5)]"></div>
             <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-widest">Patching system core & AI definitions...</span>
          </div>
          <div className="h-1 flex-1 mx-6 bg-slate-800 rounded-full overflow-hidden max-w-[200px]">
            <motion.div 
              className="h-full bg-cyan-500" 
              animate={{ width: `${systemStatus.updateProgress}%` }}
            />
          </div>
          <span className="text-[9px] font-mono text-cyan-600">EST_REMAINING: {(10 - (systemStatus.updateProgress / 10))}s</span>
        </motion.div>
      )}

      {/* Security Operations Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* RDP LINK CARD */}
          <div 
            onClick={onLaunchDesktop}
            className="group relative h-48 immersive-card bg-[#0a0f18] border-slate-800/50 flex flex-col justify-between overflow-hidden cursor-pointer"
          >
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_rgba(6,182,212,0.1)_0%,_transparent_70%)]" />
            
            <div className="relative p-8 flex flex-col h-full justify-between">
               <div className="flex justify-between items-start">
                 <div className="space-y-1">
                   <div className="flex items-center gap-2">
                       <Monitor className="w-5 h-5 text-cyan-500 active-indicator" />
                       <h3 className="font-black text-xl text-white tracking-tighter italic">LAUNCH_CLOUD_DESK</h3>
                   </div>
                   <p className="text-[10px] text-slate-500 font-mono tracking-[0.2em] uppercase">KALI_LINUX_QT6_INSTANCE // SESSION: RDP-01</p>
                 </div>
                 <div className="p-3 bg-slate-900 border border-slate-800 rounded-full text-cyan-500 group-hover:scale-110 group-hover:border-cyan-500/50 transition-all shadow-xl">
                    <ExternalLink className="w-4 h-4" />
                 </div>
               </div>

               <div className="flex gap-10 items-end">
                  <div className="space-y-1">
                     <div className="text-[8px] font-mono text-slate-600 uppercase tracking-widest">Protocol</div>
                     <div className="text-[11px] font-bold text-slate-300">RDP / AES-256GCM</div>
                  </div>
                  <div className="space-y-1">
                     <div className="text-[8px] font-mono text-slate-600 uppercase tracking-widest">Security</div>
                     <div className="text-[11px] font-bold text-emerald-500 uppercase tracking-tighter">Verified End-to-End</div>
                  </div>
                  <div className="flex-1 text-right">
                     <div className="inline-flex items-center gap-2 px-3 py-1 bg-cyan-500/10 border border-cyan-500/20 rounded-full text-[9px] font-bold text-cyan-400 tracking-widest uppercase">
                        Tunnel Secured
                     </div>
                  </div>
               </div>
            </div>
            <div className="absolute inset-0 pointer-events-none opacity-[0.03] bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,118,0.06))] bg-[length:100%_2px,3px_100%]" />
          </div>

          {/* Activity Feed and Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
             <div className="immersive-card p-6 bg-slate-900/10 h-[300px] flex flex-col">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                    <Terminal className="w-4 h-4 text-cyan-500" />
                    Kernel Logs
                  </h3>
                  <div className="flex gap-1">
                     {[1, 2, 3].map(i => <div key={i} className="w-1 h-1 rounded-full bg-cyan-500/30" />)}
                  </div>
                </div>
                <div className="flex-1 space-y-3 font-mono text-[9px] text-slate-600 uppercase overflow-hidden relative">
                   {logs.map((log, i) => (
                     <div key={i} className="flex gap-3 border-l border-slate-800/50 pl-3">
                       <span className="text-slate-800">[{new Date(log.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}]</span>
                       <span className={log.level === 'success' ? 'text-emerald-400' : 'text-slate-500'}>{log.message}</span>
                     </div>
                   ))}
                   <div className="absolute bottom-0 left-0 right-0 h-10 bg-gradient-to-t from-slate-950/20 to-transparent" />
                </div>
             </div>

             <div className="immersive-card p-6 flex flex-col justify-between">
                <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4">Neural Resource Distribution</h3>
                <div className="space-y-6">
                   {[
                     { name: 'Identity Ghosting', val: 92, col: 'bg-emerald-500' },
                     { name: 'Neural Tunneling', val: 74, col: 'bg-cyan-500' },
                     { name: 'Matrix Obfuscation', val: 32, col: 'bg-indigo-500' },
                   ].map((s, i) => (
                     <div key={i} className="space-y-2">
                        <div className="flex justify-between text-[9px] font-bold uppercase tracking-widest">
                           <span className="text-slate-500">{s.name}</span>
                           <span className="text-slate-300">{s.val}%</span>
                        </div>
                        <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                           <motion.div initial={{ width: 0 }} animate={{ width: `${s.val}%` }} className={`h-full ${s.col}`} />
                        </div>
                     </div>
                   ))}
                </div>
                <div className="pt-6 border-t border-slate-800/50 mt-4">
                   <div className="flex items-center gap-3 text-emerald-500">
                      <CheckCircle className="w-4 h-4" />
                      <span className="text-[9px] font-black uppercase tracking-widest">Subsystems Normalized</span>
                   </div>
                </div>
             </div>
          </div>
        </div>

        {/* IDS ALERT CENTER */}
        <div className="lg:col-span-1">
          <IDSAlerts />
        </div>
      </div>
    </div>
  );
};
