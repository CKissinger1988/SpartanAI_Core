import React, { useState, useEffect } from 'react';

const ipcRenderer = (typeof window !== 'undefined' && window.electronAPI)
    ? window.electronAPI.ipcRenderer
    : { invoke: async () => [] };

const IoTDashboard = () => {
    const [devices, setDevices] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const scanNetwork = async () => {
        setLoading(true);
        setError('');
        try {
            const result = await ipcRenderer.invoke('iot.manage', { action: 'scan' });
            if (Array.isArray(result)) {
                setDevices(result);
            } else {
                setError('SCAN FAILED: ENGINE ERROR');
            }
        } catch (err) {
            setError('DISCOVERY LINK OFFLINE');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        scanNetwork();
    }, []);

    const engageDevice = async (device) => {
        // AI-Driven Engagement: Analyze device properties for vulnerabilities
        const prompt = `analyze iot device: ${device.name} at ${device.addresses[0]} type ${device.type}. Properties: ${JSON.stringify(device.properties)}`;
        ipcRenderer.send('terminal.keystroke', `jarvis ${prompt}\r`);
        alert(`ENGAGEMENT INITIATED: Analyzing ${device.name} for weak vectors...`);
    };

    const containerStyle = {
        padding: '20px',
        color: '#00AAFF',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px'
    };

    const gridStyle = {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
        gap: '15px'
    };

    const cardStyle = {
        background: 'rgba(0, 170, 255, 0.05)',
        border: '1px solid rgba(0, 170, 255, 0.2)',
        padding: '15px',
        position: 'relative',
        transition: 'all 0.3s'
    };

    return (
        <div style={containerStyle}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #00AAFF', paddingBottom: '10px' }}>
                <h2 style={{ margin: 0, letterSpacing: '2px' }}>SMART_VECTORS // IoT DISCOVERY</h2>
                <button 
                    onClick={scanNetwork}
                    style={{ background: 'rgba(0, 170, 255, 0.2)', border: '1px solid #00AAFF', color: '#00AAFF', padding: '5px 15px', cursor: 'pointer', fontWeight: 'bold' }}
                    disabled={loading}
                >
                    {loading ? 'SCANNING_GRID...' : 'SCAN_NETWORK'}
                </button>
            </div>

            {error && <div style={{ color: '#ff0000', border: '1px solid #ff0000', padding: '10px' }}>&gt; {error}</div>}

            <div style={{ flex: 1, overflowY: 'auto' }}>
                <div style={gridStyle}>
                    {devices.map((dev, i) => (
                        <div key={i} style={cardStyle} onMouseEnter={e => e.currentTarget.style.borderColor = '#00AAFF'} onMouseLeave={e => e.currentTarget.style.borderColor = 'rgba(0, 170, 255, 0.2)'}>
                            <div style={{ fontSize: '10px', color: 'rgba(0, 170, 255, 0.2)', position: 'absolute', top: '5px', right: '10px' }}>{dev.type}</div>
                            <div style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '10px' }}>{dev.name.split('.')[0]}</div>
                            <div style={{ fontSize: '12px', color: 'rgba(0, 170, 255, 0.8)' }}>IP: {dev.addresses[0]}</div>
                            <div style={{ fontSize: '12px', color: 'rgba(0, 170, 255, 0.8)' }}>PORT: {dev.port}</div>
                            
                            <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
                                <button 
                                    onClick={() => engageDevice(dev)}
                                    style={{ background: '#00AAFF', color: '#000', border: 'none', padding: '5px 10px', fontSize: '10px', fontWeight: 'bold', cursor: 'pointer', flex: 1 }}
                                >
                                    AI_ENGAGE
                                </button>
                                <button 
                                    style={{ background: 'transparent', color: '#00AAFF', border: '1px solid #00AAFF', padding: '5px 10px', fontSize: '10px', cursor: 'pointer', flex: 1 }}
                                    onClick={() => alert(`PROPERTIES:\n${JSON.stringify(dev.properties, null, 2)}`)}
                                >
                                    INTEL
                                </button>
                            </div>
                        </div>
                    ))}
                    {devices.length === 0 && !loading && (
                        <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '40px', border: '1px dashed rgba(0, 170, 255, 0.05)', color: 'rgba(0, 170, 255, 0.05)' }}>
                            NO SMART VECTORS DETECTED IN LOCAL BROADCAST DOMAIN.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default IoTDashboard;
