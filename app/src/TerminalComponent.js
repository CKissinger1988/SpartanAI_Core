import React, { useEffect, useRef } from 'react';
import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import '@xterm/xterm/css/xterm.css';

const ipcRenderer = (typeof window !== 'undefined' && window.electronAPI)
    ? window.electronAPI.ipcRenderer
    : { on: () => {}, send: () => {}, removeAllListeners: () => {}, invoke: async () => ({}) };

const TerminalComponent = () => {
    const termRef = useRef(null);

    useEffect(() => {
        const term = new Terminal({
            theme: {
                background: '#000000',
                foreground: '#00ff00'
            },
            fontFamily: 'monospace'
        });
        const fitAddon = new FitAddon();
        term.loadAddon(fitAddon);
        term.open(termRef.current);
        fitAddon.fit();

        // Handle incoming data from backend
        ipcRenderer.on('terminal.incomingData', (event, data) => {
            term.write(data);
        });

        // Handle keystrokes to backend
        term.onData(data => {
            ipcRenderer.send('terminal.keystroke', data);
        });

        return () => {
            term.dispose();
            ipcRenderer.removeAllListeners('terminal.incomingData');
        };
    }, []);

    return <div ref={termRef} style={{ height: '100%', background: '#000' }} />;
};

export default TerminalComponent;
