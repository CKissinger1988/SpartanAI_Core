import React from 'react';
import styled, { keyframes } from 'styled-components';
import { Terminal, Shield, Zap, Search, HardDrive, RefreshCw, Bot } from 'lucide-react';

const popIn = keyframes`
    0% { transform: scale(0.9); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
`;

const Root = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    padding: 30px;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
`;

const ToolCard = styled.div`
    ${props => props.theme.effects.glass}
    background: ${props => props.theme.colors.glass};
    padding: 30px 20px;
    text-align: center;
    cursor: pointer;
    border-radius: 20px;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    animation: ${popIn} 0.4s ease-out backwards;
    animation-delay: ${props => props.index * 0.04}s;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;

    &:hover {
        transform: translateY(-8px);
        box-shadow: ${props => props.theme.effects.shadow};
        border-color: ${props => props.theme.colors.primary};
    }

    &:active {
        transform: scale(0.95);
    }
`;

const IconWrapper = styled.div`
    width: 60px;
    height: 60px;
    background: ${props => props.theme.colors.bg};
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: ${props => props.theme.colors.primary};
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);
    margin-bottom: 5px;
`;

const ToolName = styled.div`
    color: ${props => props.theme.colors.text};
    font-size: 1.1rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
`;

const ToolCmd = styled.div`
    color: ${props => props.theme.colors.textSecondary};
    font-size: 0.65rem;
    font-family: 'Fira Code', monospace;
    opacity: 0.7;
    word-break: break-all;
`;

const ipcRenderer = (typeof window !== 'undefined' && window.electronAPI)
    ? window.electronAPI.ipcRenderer
    : { send: () => {}, invoke: async () => ({}) };

const ToolDashboard = () => {
    const tools = [
        { name: 'AI Analyze', cmd: 'analyze status', icon: <Search size={24} /> },
        { name: 'AI Assimilation', cmd: 'assimilate ai', icon: <Bot size={24} /> },
        { name: 'Auto Exploit', cmd: 'exploit-run CVE-2021-44228', icon: <Zap size={24} /> },
        { name: 'Nmap', cmd: 'nmap -v localhost', icon: <Terminal size={24} /> },
        { name: 'Metasploit', cmd: 'msfconsole -q -x "help"', icon: <Shield size={24} /> },
        { name: 'SQLMap', cmd: 'sqlmap --version', icon: <HardDrive size={24} /> },
        { name: 'Airmon-ng', cmd: 'airmon-ng --version', icon: <RefreshCw size={24} /> },
        { name: 'Update Sys', cmd: 'sudo apt update', icon: <RefreshCw size={24} /> }
    ];

    const runTool = async (cmd) => {
        if (cmd.startsWith('analyze') || cmd.startsWith('assimilate')) {
            const response = await ipcRenderer.invoke('ai.command', cmd);
            // In production, we'd use a themed dialog
        } else if (cmd.startsWith('exploit-run')) {
            const query = cmd.replace('exploit-run ', '');
            const exploit = await ipcRenderer.invoke('exploit.manage', { action: 'find', payload: query });
            if (exploit && exploit.content) {
                ipcRenderer.send('terminal.keystroke', `# AUTO-EXPLOIT ENGAGED: ${exploit.name}\r`);
                ipcRenderer.send('tool.run', `exploit-launch --cve ${exploit.cve} --payload-data "${btoa(exploit.content)}"`);
            }
        } else {
            ipcRenderer.send('tool.run', cmd);
        }
    };

    return (
        <Root>
            {tools.map((tool, i) => (
                <ToolCard 
                    key={tool.name} 
                    index={i}
                    onClick={() => runTool(tool.cmd)}
                >
                    <IconWrapper>
                        {tool.icon}
                    </IconWrapper>
                    <ToolName>{tool.name}</ToolName>
                    <ToolCmd>{tool.cmd}</ToolCmd>
                </ToolCard>
            ))}
        </Root>
    );
};

export default ToolDashboard;
