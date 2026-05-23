import React, { useState } from 'react';
import styled, { keyframes, css } from 'styled-components';

const scanline = keyframes`
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100%); }
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
    background-color: #E8EDF2;
    background-image: radial-gradient(circle at 50% 50%, #FFFFFF 0%, #E8EDF2 100%);
    color: #2C3E50;
    font-family: 'Inter', sans-serif;
    position: relative;
    overflow: hidden;

    &::after {
        content: "";
        position: absolute;
        top: -50%; left: -50%; width: 200%; height: 200%;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
        opacity: 0.05;
        animation: ${noise} 0.5s steps(1) infinite;
        pointer-events: none;
    }
`;

const LoginBox = styled.div`
    width: 480px;
    padding: 70px 50px;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.9);
    box-shadow: 0 15px 45px rgba(0, 100, 200, 0.1);
    border-radius: 30px;
    z-index: 100;
    display: flex;
    flex-direction: column;
    gap: 40px;
    position: relative;
`;

const Brand = styled.div`
    text-align: center;
`;

const Title = styled.h1`
    font-size: 2.8rem;
    margin: 0;
    letter-spacing: 10px;
    font-weight: 900;
    text-transform: uppercase;
    color: #34495E;
    text-shadow: 0 0 15px rgba(0, 170, 255, 0.2);
`;

const Subtitle = styled.div`
    font-size: 0.7rem;
    color: #7F8C8D;
    letter-spacing: 5px;
    margin-top: 15px;
    text-transform: uppercase;
    font-weight: 700;
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
    color: #94A3B8;
    text-transform: uppercase;
    font-weight: 800;
`;

const Input = styled.input`
    background: rgba(255, 255, 255, 0.5);
    border: 1px solid #D1D9E6;
    color: #2C3E50;
    padding: 20px;
    font-size: 1rem;
    font-family: inherit;
    outline: none;
    transition: 0.4s;
    border-radius: 15px;
    width: 100%;
    box-sizing: border-box;

    &:focus {
        border-color: #00AAFF;
        background: #fff;
        box-shadow: 0 0 20px rgba(0, 170, 255, 0.1);
    }
`;

const LoginButton = styled.button`
    background: #00AAFF;
    color: #fff;
    border: none;
    padding: 22px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 6px;
    transition: 0.4s;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0, 170, 255, 0.3);

    &:hover {
        background: #0088CC;
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(0, 170, 255, 0.4);
    }

    &:active {
        transform: translateY(0);
    }

    &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
`;

const HandshakeBar = styled.div`
    height: 4px;
    background: rgba(0, 170, 255, 0.1);
    width: 100%;
    margin-top: -15px;
    border-radius: 2px;
    position: relative;
    overflow: hidden;
    
    &::after {
        content: ""; position: absolute; left: 0; top: 0; height: 100%;
        background: #00AAFF;
        width: ${props => props.progress}%;
        transition: width 0.3s;
        box-shadow: 0 0 10px #00AAFF;
    }
`;

const ErrorMsg = styled.div`
    color: #E74C3C;
    font-size: 0.7rem;
    text-align: center;
    padding: 15px;
    background: rgba(231, 76, 60, 0.05);
    border: 1px solid rgba(231, 76, 60, 0.2);
    border-radius: 12px;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 700;
`;

const Footer = styled.div`
    margin-top: 5px;
    font-size: 0.6rem;
    color: #BDC3C7;
    text-align: center;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 600;
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
                            disabled={loading}
                            placeholder="Authorize..."
                        />
                    </InputGroup>

                    {loading && <HandshakeBar progress={progress} />}
                    {error && <ErrorMsg>&gt; {error}</ErrorMsg>}

                    <LoginButton type="submit" disabled={loading}>
                        {loading ? 'SYNCHRONIZING...' : 'ESTABLISH_UPLINK'}
                    </LoginButton>
                </Form>

                <Footer>
                    ENCRYPTED VIA APEXVAULT // JARVIS OS v8.0
                </Footer>
            </LoginBox>
        </Root>
    );
};

export default LoginComponent;
