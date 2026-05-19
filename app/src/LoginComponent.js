import React, { useState } from 'react';

const ipcRenderer = (typeof window !== 'undefined' && window.electronAPI)
    ? window.electronAPI.ipcRenderer
    : { invoke: async () => ({ status: 'error', message: 'IPC NOT AVAILABLE' }) };

const LoginComponent = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        
        try {
            const result = await ipcRenderer.invoke('auth.login', { username, password });
            if (result.status === 'success') {
                onLogin(result);
            } else {
                setError(result.message || 'ACCESS DENIED');
            }
        } catch (err) {
            setError('SYSTEM FAILURE: AUTH LINK OFFLINE');
        } finally {
            setLoading(false);
        }
    };

    const containerStyle = {
        height: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        background: '#000',
        color: '#00ff00',
        fontFamily: 'monospace',
        position: 'relative',
        overflow: 'hidden'
    };

    const loginBoxStyle = {
        width: '400px',
        padding: '40px',
        background: 'rgba(10, 10, 10, 0.9)',
        border: '2px solid #00ff00',
        boxShadow: '0 0 20px rgba(0, 255, 0, 0.3)',
        zIndex: 2,
        display: 'flex',
        flexDirection: 'column',
        gap: '20px'
    };

    const inputStyle = {
        background: '#000',
        border: '1px solid #005500',
        color: '#00ff00',
        padding: '12px',
        fontSize: '16px',
        fontFamily: 'monospace',
        outline: 'none',
        transition: 'border 0.3s'
    };

    const btnStyle = {
        background: '#005500',
        color: '#00ff00',
        border: '1px solid #00ff00',
        padding: '12px',
        cursor: 'pointer',
        fontSize: '16px',
        fontWeight: 'bold',
        textTransform: 'uppercase',
        letterSpacing: '2px',
        marginTop: '10px'
    };

    return (
        <div style={containerStyle}>
            <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', opacity: 0.1, pointerEvents: 'none', background: 'repeating-linear-gradient(0deg, #00ff00 0px, transparent 1px, transparent 2px)' }} />
            
            <div style={loginBoxStyle}>
                <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                    <h1 style={{ fontSize: '28px', margin: 0, letterSpacing: '4px' }}>NEXUS // AI</h1>
                    <div style={{ fontSize: '10px', color: '#005500' }}>RESTRICTED ACCESS TERMINAL</div>
                </div>

                <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                        <label htmlFor="operator-id" style={{ fontSize: '12px' }}>[ OPERATOR_ID ]</label>
                        <input 
                            id="operator-id"
                            style={inputStyle}
                            type="text" 
                            value={username} 
                            onChange={(e) => setUsername(e.target.value)}
                            onFocus={(e) => e.target.style.borderColor = '#00ff00'}
                            onBlur={(e) => e.target.style.borderColor = '#005500'}
                            disabled={loading}
                        />
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                        <label htmlFor="access-key" style={{ fontSize: '12px' }}>[ ACCESS_KEY ]</label>
                        <input 
                            id="access-key"
                            style={inputStyle}
                            type="password" 
                            value={password} 
                            onChange={(e) => setPassword(e.target.value)}
                            onFocus={(e) => e.target.style.borderColor = '#00ff00'}
                            onBlur={(e) => e.target.style.borderColor = '#005500'}
                            disabled={loading}
                        />
                    </div>

                    {error && (
                        <div style={{ color: '#ff0000', fontSize: '12px', textAlign: 'center', padding: '5px', border: '1px solid #ff0000', background: 'rgba(255,0,0,0.1)' }}>
                            &gt; {error}
                        </div>
                    )}

                    <button 
                        type="submit" 
                        style={{...btnStyle, opacity: loading ? 0.5 : 1}} 
                        disabled={loading}
                    >
                        {loading ? 'AUTHENTICATING...' : 'INIT_UPLINK'}
                    </button>
                </form>

                <div style={{ marginTop: '20px', fontSize: '10px', color: '#003300', textAlign: 'center' }}>
                    WARNING: UNAUTHORIZED ACCESS ATTEMPTS ARE MONITORED AND LOGGED.
                </div>
            </div>
        </div>
    );
};

export default LoginComponent;
