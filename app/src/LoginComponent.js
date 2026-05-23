import React, { useState } from 'react';
import styled, { keyframes, css } from 'styled-components';

const scanline = keyframes`
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100%); }
`;

const intensePulse = keyframes`
    0% { box-shadow: 0 0 10px rgba(0, 170, 255, 0.4); }
    50% { box-shadow: 0 0 25px rgba(0, 170, 255, 0.8); }
    100% { box-shadow: 0 0 10px rgba(0, 170, 255, 0.4); }
`;

const noise = keyframes`
    0% { transform: translate(0,0) }
    10% { transform: translate(-5%,-5%) }
    20% { transform: translate(-10%,5%) }
    30% { transform: translate(5%,-10%) }
    40% { transform: translate(-5%,15%) }
    50% { transform: translate(-10%,5%) }
    60% { transform: translate(15%,0) }
    70% { transform: translate(0,10%) }
    80% { transform: translate(-15%,0) }
    90% { transform: translate(10%,5%) }
    100% { transform: translate(5%,0) }
`;

const Root = styled.div`
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #000;
    color: #00AAFF;
    font-family: 'Fira Code', monospace;
    position: relative;
    overflow: hidden;

    &::after {
        content: "";
        position: absolute;
        top: -50%; left: -50%; width: 200%; height: 200%;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
        opacity: 0.03;
        animation: ${noise} 0.5s steps(1) infinite;
        pointer-events: none;
    }
`;

const Scanline = styled.div`
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(to bottom, transparent 50%, rgba(0, 170, 255, 0.02) 50.5%);
    background-size: 100% 4px;
    pointer-events: none;
    z-index: 10;
`;

const MovingScanline = styled.div`
    position: absolute;
    top: 0; left: 0; width: 100%; height: 2px;
    background: rgba(0, 170, 255, 0.2);
    animation: ${scanline} 8s linear infinite;
    z-index: 11;
`;

const LoginBox = styled.div`
    width: 450px;
    padding: 60px 40px;
    background: rgba(2, 2, 2, 0.98);
    border: 1px solid #00AAFF;
    box-shadow: 0 0 60px rgba(0, 170, 255, 0.15);
    z-index: 100;
    display: flex;
    flex-direction: column;
    gap: 30px;
    backdrop-filter: blur(40px);
    position: relative;

    &::before {
        content: ""; position: absolute; top: -1px; left: -1px; right: -1px; bottom: -1px;
        background: linear-gradient(45deg, #00AAFF, transparent, #00AAFF);
        opacity: 0.1;
        pointer-events: none;
    }
`;

const Brand = styled.div`
    text-align: center;
`;

const Title = styled.h1`
    font-size: 2.4rem;
    margin: 0;
    letter-spacing: 16px;
    font-weight: 900;
    text-transform: uppercase;
    color: #fff;
    text-shadow: 0 0 20px #00AAFF;
`;

const Subtitle = styled.div`
    font-size: 0.6rem;
    color: #00AAFF;
    letter-spacing: 6px;
    margin-top: 12px;
    opacity: 0.5;
    text-transform: uppercase;
`;

const Form = styled.form`
    display: flex;
    flex-direction: column;
    gap: 25px;
`;

const InputGroup = styled.div`
    display: flex;
    flex-direction: column;
    gap: 10px;
`;

const Label = styled.label`
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: #444;
    text-transform: uppercase;
`;

const Input = styled.input`
    background: rgba(255, 255, 255, 0.01);
    border: 1px solid #111;
    color: #fff;
    padding: 16px;
    font-size: 0.9rem;
    font-family: inherit;
    outline: none;
    transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 2px;

    &:focus {
        border-color: #00AAFF;
        background: rgba(0, 170, 255, 0.03);
        box-shadow: 0 0 ${props => Math.min(30, props.valueLength * 2)}px rgba(0, 170, 255, 0.2);
    }
`;

const LoginButton = styled.button`
    background: transparent;
    color: #00AAFF;
    border: 1px solid #00AAFF;
    padding: 20px;
    cursor: pointer;
    font-size: 0.75rem;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 5px;
    transition: 0.4s;
    border-radius: 2px;
    margin-top: 10px;
    position: relative;
    overflow: hidden;

    &::after {
        content: ""; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 170, 255, 0.2), transparent);
        transition: 0.5s;
    }

    &:hover {
        background: rgba(0, 170, 255, 0.05);
        color: #fff;
        box-shadow: 0 0 40px rgba(0, 170, 255, 0.3);
        &::after { left: 100%; }
    }

    &:disabled {
        opacity: 0.3;
        cursor: not-allowed;
    }
`;

const HandshakeBar = styled.div`
    height: 1px;
    background: rgba(0, 170, 255, 0.1);
    width: 100%;
    margin-top: -15px;
    position: relative;
    
    &::after {
        content: ""; position: absolute; left: 0; top: 0; height: 100%;
        background: #00AAFF;
        width: ${props => props.progress}%;
        transition: width 0.3s;
        box-shadow: 0 0 10px #00AAFF;
    }
`;

const ErrorMsg = styled.div`
    color: #ff3b3b;
    font-size: 0.65rem;
    text-align: center;
    padding: 12px;
    background: rgba(255, 59, 59, 0.05);
    border: 1px solid rgba(255, 59, 59, 0.2);
    letter-spacing: 2px;
    text-transform: uppercase;
`;

const Footer = styled.div`
    margin-top: 5px;
    font-size: 0.55rem;
    color: #222;
    text-align: center;
    letter-spacing: 2px;
    text-transform: uppercase;
`;

const ipcRenderer = (typeof window !== 'undefined' && window.electronAPI)
    ? window.electronAPI.ipcRenderer
    : { invoke: async () => ({ status: 'error', message: 'IPC NOT AVAILABLE' }) };

const LoginComponent = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setProgress(10);
        
        // Simulate high-integrity handshake stages
        const steps = [30, 65, 90];
        for(let s of steps) {
            await new Promise(r => setTimeout(r, 400));
            setProgress(s);
        }

        try {
            const result = await ipcRenderer.invoke('auth.login', { username, password });
            setProgress(100);
            if (result.status === 'success') {
                onLogin(result);
            } else {
                setError(result.message || 'ACCESS DENIED');
                setProgress(0);
            }
        } catch (err) {
            setError('SYSTEM FAILURE: AUTH LINK OFFLINE');
            setProgress(0);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Root>
            <Scanline />
            <MovingScanline />
            
            <LoginBox>
                <Brand>
                    <Title>SENTINELAI</Title>
                    <Subtitle>Supreme Intelligence Portal</Subtitle>
                </Brand>

                <Form onSubmit={handleLogin}>
                    <InputGroup>
                        <Label htmlFor="operator-id">[ OPERATOR_ID ]</Label>
                        <Input 
                            id="operator-id"
                            type="text" 
                            value={username} 
                            onChange={(e) => setUsername(e.target.value)}
                            valueLength={username.length}
                            disabled={loading}
                            autoComplete="off"
                            placeholder="Identify..."
                        />
                    </InputGroup>

                    <InputGroup>
                        <Label htmlFor="access-key">[ ACCESS_KEY ]</Label>
                        <Input 
                            id="access-key"
                            type="password" 
                            value={password} 
                            onChange={(e) => setPassword(e.target.value)}
                            valueLength={password.length}
                            disabled={loading}
                            placeholder="Authorize..."
                        />
                    </InputGroup>

                    {loading && <HandshakeBar progress={progress} />}
                    {error && <ErrorMsg>&gt; {error}</ErrorMsg>}

                    <LoginButton type="submit" disabled={loading}>
                        {loading ? 'SYNCING...' : 'ESTABLISH_UPLINK'}
                    </LoginButton>
                </Form>

                <Footer>
                    ENCRYPTED VIA APEXVAULT // ZERO TRUST ACTIVE.
                </Footer>
            </LoginBox>
        </Root>
    );
};

export default LoginComponent;
