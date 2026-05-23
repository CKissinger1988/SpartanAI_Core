import React, { useState, useEffect, useRef } from 'react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebglAddon } from 'xterm-addon-webgl';
import 'xterm/css/xterm.css';

const SentinelHub = () => {
  const termRef = useRef(null);
  const fitAddon = useRef(new FitAddon());
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => {
    const term = new Terminal({ fontSize: 14 });
    term.loadAddon(fitAddon.current);
    term.loadAddon(new WebglAddon());
    term.open(termRef.current);
    fitAddon.current.fit();

    const handleResize = () => {
      fitAddon.current.fit();
    };
    window.addEventListener('resize', handleResize);

    // In a real implementation, connect to node-pty here
    term.write('Sentinel Hub Terminal Ready...');

    return () => {
      window.removeEventListener('resize', handleResize);
      term.dispose();
    };
  }, []);

  return (
    <div style={{ display: 'flex', height: '100vh', background: '#1e1e1e', color: 'white' }}>
      <nav style={{ width: '200px', padding: '20px', borderRight: '1px solid #333' }}>
        <h2>Sentinel Hub</h2>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li onClick={() => setActiveTab('dashboard')} style={{ cursor: 'pointer', padding: '10px' }}>Dashboard</li>
          <li onClick={() => setActiveTab('chat')} style={{ cursor: 'pointer', padding: '10px' }}>AI Chat</li>
          <li onClick={() => setActiveTab('rdp')} style={{ cursor: 'pointer', padding: '10px' }}>Kali RDP</li>
        </ul>
      </nav>
      <main style={{ flex: 1, padding: '20px' }}>
        {activeTab === 'dashboard' && <div ref={termRef} style={{ height: '600px' }} />}
        {activeTab === 'chat' && <div>AI Chat Interface Placeholder</div>}
        {activeTab === 'rdp' && <div>RDP Viewer Placeholder</div>}
      </main>
    </div>
  );
};

export default SentinelHub;
