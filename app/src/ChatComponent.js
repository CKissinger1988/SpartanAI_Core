import React, { useState, useRef, useEffect } from 'react';

const ipcRenderer = (typeof window !== 'undefined' && window.electronAPI)
    ? window.electronAPI.ipcRenderer
    : { invoke: async () => 'IPC NOT AVAILABLE' };

const ChatComponent = () => {
    const [messages, setMessages] = useState([
        { sender: 'SYSTEM', text: 'NEXUS CORE ONLINE. READY FOR INSTRUCTIONS.' }
    ]);
    const [input, setInput] = useState('');
    const scrollRef = useRef(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim()) return;
        const currentInput = input;
        setInput('');
        
        const userMsg = { sender: 'OPERATOR', text: currentInput };
        setMessages(prev => [...prev, userMsg]);
        
        try {
            const response = await ipcRenderer.invoke('ai.command', currentInput);
            setMessages(prev => [...prev, { sender: 'SYSTEM', text: response }]);
        } catch (error) {
            setMessages(prev => [...prev, { sender: 'SYSTEM', text: `ERROR: ${error.message}` }]);
        }
    };

    const containerStyle = {
        height: 'calc(100vh - 80px)',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        padding: '20px',
        background: 'rgba(0,0,0,0.8)'
    };

    const messageBoxStyle = {
        flex: 1,
        border: '1px solid #005500',
        padding: '20px',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '10px'
    };

    const inputStyle = {
        background: '#0a0a0a',
        border: '1px solid #00ff00',
        color: '#00ff00',
        padding: '15px',
        fontFamily: 'monospace',
        fontSize: '16px',
        outline: 'none',
        width: '100%'
    };

    return (
        <div style={containerStyle}>
            <div style={messageBoxStyle} ref={scrollRef}>
                {messages.map((m, i) => (
                    <div key={i} style={{ marginBottom: '10px', animation: 'fadeIn 0.5s', whiteSpace: 'pre-wrap' }}>
                        <span style={{ color: m.sender === 'SYSTEM' ? '#00ff00' : '#00aa00', fontWeight: 'bold' }}>
                            [{m.sender}]>
                        </span>
                        <span style={{ marginLeft: '10px', color: '#fff' }}>{m.text}</span>
                    </div>
                ))}
            </div>
            <div style={{ display: 'flex', gap: '10px' }}>
                <input 
                    style={inputStyle}
                    value={input} 
                    placeholder="ENTER COMMAND..."
                    onChange={(e) => setInput(e.target.value)} 
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()} 
                />
                <button 
                    onClick={sendMessage}
                    style={{ background: '#00ff00', color: '#000', border: 'none', padding: '0 30px', cursor: 'pointer', fontWeight: 'bold' }}
                >
                    SEND
                </button>
            </div>
        </div>
    );
};

export default ChatComponent;
