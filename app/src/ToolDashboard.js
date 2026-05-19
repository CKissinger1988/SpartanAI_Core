import React from 'react';

const ipcRenderer = (typeof window !== 'undefined' && window.electronAPI)
    ? window.electronAPI.ipcRenderer
    : { send: () => {}, invoke: async () => ({}) };

const ToolDashboard = () => {
    const tools = [
        { name: 'AI Analyze', cmd: 'analyze status' },
        { name: 'Auto Exploit', cmd: 'exploit-run CVE-2021-44228' },
        { name: 'Nmap', cmd: 'nmap -v localhost' },
        { name: 'Metasploit', cmd: 'msfconsole -q -x "help"' },
        { name: 'SQLMap', cmd: 'sqlmap --version' },
        { name: 'Airmon-ng', cmd: 'airmon-ng --version' },
        { name: 'Update Sys', cmd: 'sudo apt update' }
    ];

    const runTool = async (cmd) => {
        if (cmd.startsWith('analyze')) {
            // Trigger AI analysis directly
            const response = await ipcRenderer.invoke('ai.command', cmd);
            alert(`AI Analysis:\n${response}`);
        } else if (cmd.startsWith('exploit-run')) {
            const query = cmd.replace('exploit-run ', '');
            const exploit = await ipcRenderer.invoke('exploit.manage', { action: 'find', payload: query });
            if (exploit && exploit.content) {
                // In a real offensive OS, we'd save this to a temp file and execute it
                // For now, we'll pipe the instruction to the terminal to show the "intent"
                ipcRenderer.send('terminal.keystroke', `# AUTO-EXPLOIT ENGAGED: ${exploit.name}\r`);
                ipcRenderer.send('terminal.keystroke', `# SOURCE: ${exploit.url}\r`);
                // Simulate execution start
                ipcRenderer.send('tool.run', `echo "Executing ${exploit.cve} payload..."`);
            } else {
                alert(`Exploit for '${query}' not found in database.`);
            }
        } else {
            ipcRenderer.send('tool.run', cmd);
        }
    };

    const containerStyle = {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
        gap: '20px',
        padding: '20px'
    };

    const cardStyle = {
        background: '#0a0a0a',
        border: '1px solid #005500',
        padding: '15px',
        textAlign: 'center',
        cursor: 'pointer',
        transition: 'all 0.3s'
    };

    return (
        <div style={containerStyle}>
            {tools.map(tool => (
                <div 
                    key={tool.name} 
                    style={cardStyle} 
                    onClick={() => runTool(tool.cmd)}
                    onMouseEnter={(e) => e.currentTarget.style.borderColor = '#00ff00'}
                    onMouseLeave={(e) => e.currentTarget.style.borderColor = '#005500'}
                >
                    <div style={{ color: '#00ff00', fontSize: '18px', marginBottom: '10px' }}>{tool.name}</div>
                    <div style={{ color: '#005500', fontSize: '10px' }}>{tool.cmd}</div>
                </div>
            ))}
        </div>
    );
};

export default ToolDashboard;
