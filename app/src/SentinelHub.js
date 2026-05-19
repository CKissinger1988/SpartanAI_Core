import React, { useState, useEffect } from 'react';
import TerminalComponent from './TerminalComponent';
import ChatComponent from './ChatComponent';
import ToolDashboard from './ToolDashboard';
import ExploitDB from './ExploitDB';
import MatrixBackground from './MatrixBackground';

const ipcRenderer = (typeof window !== 'undefined' && window.electronAPI) 
    ? window.electronAPI.ipcRenderer 
    : { invoke: () => Promise.resolve({ cpu: 0, mem: 0 }), on: () => {}, send: () => {} };

const SentinelHub = () => {
    const [activeTab, setActiveTab] = useState('Terminal');
    const [stats, setStats] = useState({ cpu: 0, mem: 0 });

    useEffect(() => {
        const interval = setInterval(async () => {
            const newStats = await ipcRenderer.invoke('system.getStats');
            setStats(newStats);
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    const navStyle = {
        width: '240px',
        background: 'rgba(10, 10, 10, 0.9)',
        color: '#00ff00',
        padding: '20px',
        display: 'flex',
        flexDirection: 'column',
        gap: '15px',
        borderRight: '2px solid #00ff00',
        boxShadow: '0 0 15px rgba(0, 255, 0, 0.2)',
        zIndex: 1
    };

    const statStyle = {
        fontSize: '12px',
        color: '#00ff00',
        padding: '10px',
        border: '1px dotted #00ff00',
        marginBottom: '10px',
        background: 'rgba(0,0,0,0.5)'
    };

    const buttonStyle = (tab) => ({
        background: activeTab === tab ? '#00ff0022' : 'rgba(0,0,0,0.5)',
        color: activeTab === tab ? '#00ff00' : '#00aa00',
        border: `1px solid ${activeTab === tab ? '#00ff00' : '#005500'}`,
        padding: '12px',
        cursor: 'pointer',
        textAlign: 'left',
        outline: 'none',
        fontSize: '14px',
        borderRadius: '2px',
        textTransform: 'uppercase',
        letterSpacing: '1px',
        transition: 'all 0.3s'
    });

    return (
        <div style={{ display: 'flex', height: '100vh', background: '#000', color: '#fff', fontFamily: 'monospace', overflow: 'hidden' }}>
            <MatrixBackground />
            <nav style={navStyle}>
                <h1 style={{ fontSize: '24px', margin: '0 0 20px 0', color: '#00ff00', textShadow: '0 0 10px #00ff00' }}>NEXUS // AI</h1>
                
                <div style={statStyle}>
                    <div>SYS LOAD: {stats.cpu.toFixed(1)}%</div>
                    <div style={{ width: '100%', height: '4px', background: '#333', marginTop: '4px' }}>
                        <div style={{ width: `${stats.cpu}%`, height: '100%', background: '#00ff00' }} />
                    </div>
                    <div style={{ marginTop: '10px' }}>MEM LOAD: {stats.mem.toFixed(1)}%</div>
                    <div style={{ width: '100%', height: '4px', background: '#333', marginTop: '4px' }}>
                        <div style={{ width: `${stats.mem}%`, height: '100%', background: '#00ff00' }} />
                    </div>
                </div>

                <button style={buttonStyle('Terminal')} onClick={() => setActiveTab('Terminal')}>[#] MAIN_SHELL</button>
                <button style={buttonStyle('Chat')} onClick={() => setActiveTab('Chat')}>[@] AI_CORE</button>
                <button style={buttonStyle('Tools')} onClick={() => setActiveTab('Tools')}>[%] TOOL_VAULT</button>
                <button style={buttonStyle('Exploits')} onClick={() => setActiveTab('Exploits')}>[!] EXPLOIT_DB</button>
                
                <div style={{ marginTop: 'auto', fontSize: '10px', color: '#005500' }}>
                    NEURAL SYNAPSE: ACTIVE<br/>
                    DEEP LEARNING: SYNCED<br/>
                    STATUS: SECURE<br/>
                    UPLINK: ACTIVE<br/>
                    VER: 2.0.0-YOLO
                </div>
            </nav>
            <main style={{ flex: 1, padding: '20px', overflow: 'hidden', position: 'relative', background: 'rgba(0,0,0,0.7)' }}>
                <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', opacity: 0.05, pointerEvents: 'none', background: 'repeating-linear-gradient(0deg, #00ff00 0px, transparent 1px, transparent 2px)' }} />
                {activeTab === 'Terminal' && <TerminalComponent />}
                {activeTab === 'Chat' && <ChatComponent />}
                {activeTab === 'Tools' && <ToolDashboard />}
                {activeTab === 'Exploits' && <ExploitDB />}
            </main>
        </div>
    );
};

export default SentinelHub;
