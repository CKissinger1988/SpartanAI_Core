import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './components/Dashboard';
import { JarvisVoice } from './components/JarvisVoice';
import { ModelManager } from './components/ModelManager';
import { SecurityLab } from './components/SecurityLab';
import { DeepLearning } from './components/DeepLearning';
import { BootSequence } from './components/BootSequence';
import { KaliTerminal } from './components/KaliTerminal';
import { RemoteDesktop } from './components/RemoteDesktop';
import { motion, AnimatePresence } from 'motion/react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { Login } from './components/Login';
import { Settings } from './components/Settings';

function AppContent() {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [notifications, setNotifications] = useState<{ id: string, text: string }[]>([]);
  const [isBooting, setIsBooting] = useState(true);
  const { user, loading } = useAuth();

  useEffect(() => {
    // Check initial server state
    fetch('/api/system/status')
      .then(res => res.json())
      .then(data => {
        if (!data.isBooting) {
          setIsBooting(false);
        }
      })
      .catch(() => {
        // If server is not ready yet, we rely on BootSequence internal polling
      });
  }, []);

  const addNotification = (text: string) => {
    const id = Math.random().toString(36).substr(2, 9);
    setNotifications(prev => [...prev, { id, text }]);
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== id));
    }, 5000);
  };

  const handleJarvisCommand = (command: string, args: any) => {
    switch (command) {
      case 'switch_tab':
        if (args.tab) {
          setActiveTab(args.tab);
          addNotification(`JARVIS: Navigating to ${args.tab.toUpperCase()}`);
        }
        break;
      case 'initiate_scan':
        setActiveTab('security');
        addNotification(`JARVIS: Initiating scan on ${args.target}`);
        break;
      case 'manage_training':
        setActiveTab('deeplearning');
        addNotification(`JARVIS: Training procedure ${args.action.toUpperCase()}ED`);
        break;
      case 'check_system_updates':
        setActiveTab('dashboard');
        if (args.mode === 'install') {
          addNotification("JARVIS: Initiating system recovery and update sequence");
          fetch('/api/system/update', { method: 'POST' }).catch(e => console.error(e));
        } else {
          addNotification("JARVIS: Polling primary repositories for security patches");
        }
        break;
      case 'execute_advanced_protocol':
        addNotification(`JARVIS: EXECUTING PROTOCOL [${args.protocol_name.toUpperCase()}]`);
        break;
      case 'automate_exploit':
        setActiveTab('security');
        addNotification("JARVIS: Identifying severe threats and preparing counter-exploit...");
        // Call the proposal endpoint immediately
        setTimeout(() => {
          window.dispatchEvent(new CustomEvent('jarvis-exploit-trigger'));
        }, 1000);
        break;
      default:
        console.log("Unknown command:", command, args);
    }
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard': return <Dashboard onLaunchDesktop={() => setActiveTab('desktop')} />;
      case 'jarvis': return <JarvisVoice onCommand={handleJarvisCommand} />;
      case 'models': return <ModelManager />;
      case 'security': return <SecurityLab />;
      case 'deeplearning': return <DeepLearning />;
      case 'terminal': return <KaliTerminal />;
      case 'desktop': return <RemoteDesktop />;
      default: return <Dashboard onLaunchDesktop={() => setActiveTab('desktop')} />;
    }
  };

  if (loading) return (
    <div className="h-screen w-full bg-[#02040a] flex items-center justify-center font-mono text-cyan-500 animate-pulse">
      INITIALIZING_SECURE_AUTH...
    </div>
  );

  return (
    <>
      <AnimatePresence mode="wait">
        {!user ? (
          <Login key="login" />
        ) : isBooting ? (
          <BootSequence key="boot" onComplete={() => setIsBooting(false)} />
        ) : (
          <motion.div 
            key="interface"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="h-screen w-full bg-[#02040a] text-slate-300 font-sans flex flex-col overflow-hidden border-2 border-slate-900"
          >
            {/* TOP NAVIGATION BAR */}
            <nav className="h-12 border-b border-cyan-900/30 bg-black/40 flex items-center justify-between px-6 shrink-0 z-50">
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-cyan-500 rounded-full shadow-[0_0_10px_rgba(6,182,212,0.8)]"></div>
                  <span className="text-xs font-mono tracking-widest text-cyan-400">NEXUS_SECURITY_CONSOLE</span>
                </div>
                <div className="h-4 w-px bg-slate-800"></div>
                <span className="text-[10px] text-slate-500 uppercase tracking-tighter hidden md:block">OPERATIONAL STATE: ACTIVE // REGION: US-WEST</span>
              </div>
              <div className="flex items-center gap-6">
                <div className="flex items-center gap-4">
                  <div className="flex flex-col items-end">
                    <span className="text-[10px] text-white uppercase font-bold">{user.displayName || 'Operator'}</span>
                    <span className="text-[8px] text-slate-500 font-mono">{user.email}</span>
                  </div>
                  <div className="w-8 h-8 rounded-full border border-cyan-500/30 flex items-center justify-center bg-slate-900 overflow-hidden">
                    <span className="text-[10px] font-bold text-cyan-500">{(user.displayName || 'OP')[0]}</span>
                  </div>
                </div>
                <div className="h-4 w-px bg-slate-800"></div>
                <div className="flex flex-col items-end">
                  <span className="text-[10px] text-emerald-500 uppercase font-bold">Network Status: NOMINAL</span>
                  <span className="text-[9px] text-slate-600">ENCRYPTION: AES-256-GCM</span>
                </div>
              </div>
            </nav>

            {/* MAIN INTERFACE */}
            <div className="flex flex-1 overflow-hidden">
              <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} onOpenSettings={() => setIsSettingsOpen(true)} />
              
              <Settings open={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />
              
              <main className="flex-1 overflow-y-auto relative p-6 bg-[radial-gradient(circle_at_top_right,_rgba(6,182,212,0.03)_0%,_transparent_50%)]">
                <div className="max-w-7xl mx-auto space-y-6">
                  <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                    {renderContent()}
                  </div>
                </div>

                {/* Global Notifications */}
                <div className="fixed bottom-12 right-6 z-50 flex flex-col gap-2 pointer-events-none">
                  <AnimatePresence>
                    {notifications.map(n => (
                      <motion.div
                        key={n.id}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 20 }}
                        className="bg-cyan-950/80 border border-cyan-500/30 backdrop-blur-md px-4 py-2 rounded text-[9px] font-mono text-cyan-400 uppercase tracking-[0.2em] shadow-[0_0_15px_rgba(6,182,212,0.1)] flex items-center gap-3"
                      >
                        <div className="w-1 h-1 bg-cyan-500 rounded-full animate-pulse" />
                        {n.text}
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </div>
              </main>
            </div>

            {/* FOOTER BAR */}
            <footer className="h-8 border-t border-slate-900 bg-black/80 flex items-center justify-between px-6 shrink-0 z-50">
              <div className="flex items-center gap-4 text-[9px] font-mono text-slate-500">
                <span className="flex items-center gap-1">
                  <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></div> 
                  SYSTEM OK
                </span>
                <span className="hidden sm:block">UPTIME: 14D 02H 11M</span>
                <span className="hidden md:block text-slate-700">|</span>
                <span className="hidden md:block">IP: [PROTECTED]</span>
                <span className="hidden md:block text-slate-700">|</span>
                <span className="text-cyan-500/70">SECURE_SYNC: AUTHENTICATED</span>
              </div>
              <div className="flex items-center gap-4 text-[9px] font-mono">
                <span className="text-slate-600 uppercase tracking-tighter">Nexus Intelligence v2.5.0-Production</span>
              </div>
            </footer>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
