import React, { useState, useEffect, useRef } from 'react';
import { Card } from 'antd';
import { AnsiUp } from 'ansi_up';

const ipcRenderer = window.electronAPI?.ipcRenderer;
const ansi_up = new AnsiUp();

const MiniTerminal = ({ title, channel }) => {
    const [output, setOutput] = useState([]);
    const contentRef = useRef(null);

    useEffect(() => {
        if (!ipcRenderer) return;
        const handleData = (event, data) => {
            setOutput(prev => [...prev.slice(-50), ansi_up.ansi_to_html(data)]);
        };
        ipcRenderer.on(channel, handleData);
        ipcRenderer.send('monitor.start', channel);
        return () => ipcRenderer.removeAllListeners(channel);
    }, [channel]);

    useEffect(() => {
        if (contentRef.current) contentRef.current.scrollTop = contentRef.current.scrollHeight;
    }, [output]);

    return (
        <Card title={title} size="small" bordered={false} style={{ background: '#020617', height: '250px' }}>
            <div 
                ref={contentRef}
                style={{ height: '100%', overflowY: 'scroll', fontFamily: 'monospace', fontSize: '11px', color: '#94a3b8', background: '#020617', padding: '8px', whiteSpace: 'pre-wrap' }}
            >
                {output.map((line, index) => <div key={index} dangerouslySetInnerHTML={{ __html: line }} />)}
            </div>
        </Card>
    );
};

export default MiniTerminal;
