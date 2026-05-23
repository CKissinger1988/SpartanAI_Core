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
`;

const Scanline = styled.div`
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(to bottom, transparent 50%, rgba(0, 170, 255, 0.05) 50.5%);
    background-size: 100% 4px;
    pointer-events: none;
    z-index: 10;
`;

const MovingScanline = styled.div`
    position: absolute;
    top: 0; left: 0; width: 100%; height: 2px;
    background: rgba(0, 170, 255, 0.2);
    animation: ${scanline} 6s linear infinite;
    z-index: 11;
`;

const LoginBox = styled.div`
    width: 450px;
    padding: 60px 40px;
    background: rgba(5, 5, 5, 0.95);
    border: 1px solid #00AAFF;
    box-shadow: 0 0 40px rgba(0, 170, 255, 0.2);
    z-index: 100;
    display: flex;
    flex-direction: column;
    gap: 30px;
    backdrop-filter: blur(20px);
    position: relative;

    &::before {
        content: ""; position: absolute; top: -2px; left: -2px; right: -2px; bottom: -2px;
        border: 1px solid rgba(0, 170, 255, 0.1); pointer-events: none;
    }
`;

const Brand = styled.div`
    text-align: center;
`;

const Title = styled.h1`
    font-size: 2.2rem;
    margin: 0;
    letter-spacing: 12px;
    font-weight: 900;
    text-transform: uppercase;
    color: #fff;
    text-shadow: 0 0 10px #00AAFF;
`;

const Subtitle = styled.div`
    font-size: 0.65rem;
    color: #00AAFF;
    letter-spacing: 4px;
    margin-top: 10px;
    opacity: 0.6;
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
    gap: 8px;
`;

const Label = styled.label`
    font-size: 0.7rem;
    letter-spacing: 2px;
    color: #888;
    text-transform: uppercase;
`;

const Input = styled.input`
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid #222;
    color: #fff;
    padding: 15px;
    font-size: 0.9rem;
    font-family: inherit;
    outline: none;
    transition: 0.3s;
    border-radius: 4px;

    &:focus {
        border-color: #00AAFF;
        background: rgba(0, 170, 255, 0.05);
        box-shadow: 0 0 15px rgba(0, 170, 255, 0.1);
    }
`;

const LoginButton = styled.button`
    background: rgba(0, 170, 255, 0.1);
    color: #00AAFF;
    border: 1px solid #00AAFF;
    padding: 18px;
    cursor: pointer;
    font-size: 0.8rem;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 4px;
    transition: 0.3s;
    border-radius: 4px;
    margin-top: 15px;
    animation: ${intensePulse} 3s infinite ease-in-out;

    &:hover {
        background: rgba(0, 170, 255, 0.2);
        color: #fff;
        box-shadow: 0 0 30px rgba(0, 170, 255, 0.4);
        transform: translateY(-2px);
    }

    &:active {
        transform: translateY(0);
    }

    &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        animation: none;
    }
`;

const ErrorMsg = styled.div`
    color: #F44336;
    font-size: 0.7rem;
    text-align: center;
    padding: 10px;
    background: rgba(244, 67, 54, 0.1);
    border: 1px solid #F44336;
    border-radius: 4px;
    letter-spacing: 1px;
`;

const Footer = styled.div`
    margin-top: 10px;
    font-size: 0.6rem;
    color: #333;
    text-align: center;
    letter-spacing: 1px;
`;

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
                            disabled={loading}
                            autoComplete="off"
                            placeholder="Enter Identity..."
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
                            placeholder="Enter Authorization..."
                        />
                    </InputGroup>

                    {error && <ErrorMsg>&gt; ERROR: {error}</ErrorMsg>}

                    <LoginButton type="submit" disabled={loading}>
                        {loading ? 'AUTHENTICATING...' : 'ESTABLISH_UPLINK'}
                    </LoginButton>
                </Form>

                <Footer>
                    SECURE CONNECTION ENCRYPTED VIA APEXVAULT // UNAUTHORIZED ACCESS IS PROHIBITED.
                </Footer>
            </LoginBox>
        </Root>
    );
};

export default LoginComponent;
