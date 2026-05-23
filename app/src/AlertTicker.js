import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { ShieldCheck, ShieldAlert, X } from 'lucide-react';

const slideDown = keyframes`
    from { transform: translateY(-100%); }
    to { transform: translateY(0); }
`;

const slideUp = keyframes`
    from { transform: translateY(0); }
    to { transform: translateY(-100%); }
`;

const Root = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 2000;
    padding: 15px 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    pointer-events: none;
`;

const Bar = styled.div`
    ${props => props.theme.effects.glass}
    background: ${props => props.alert ? props.theme.colors.error : props.theme.colors.glass};
    color: ${props => props.alert ? '#fff' : props.theme.colors.text};
    padding: 15px 40px;
    border-radius: 0 0 25px 25px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: ${props => props.theme.effects.shadow};
    animation: ${props => props.active ? slideDown : slideUp} 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    pointer-events: auto;
    min-width: 400px;
    max-width: 80%;

    svg {
        flex-shrink: 0;
    }
`;

const Message = styled.div`
    font-size: 0.9rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    flex: 1;
`;

const Dismiss = styled.div`
    cursor: pointer;
    opacity: 0.6;
    transition: 0.3s;
    padding: 10px;
    margin-right: -10px;

    &:hover {
        opacity: 1;
        transform: scale(1.1);
    }
`;

const ipcRenderer = window.electronAPI?.ipcRenderer;

const AlertTicker = () => {
    const [alert, setAlert] = useState(null);
    const [visible, setVisible] = useState(true);

    useEffect(() => {
        if (!ipcRenderer) return;
        const handleAlert = (event, newAlert) => {
            setAlert(newAlert);
            setVisible(true);
            setTimeout(() => setVisible(false), 8000);
        };
        ipcRenderer.on('system.alert', handleAlert);
        return () => ipcRenderer.removeAllListeners('system.alert');
    }, []);

    const content = alert ? (
        <Bar alert active={visible}>
            <ShieldAlert size={20} />
            <Message>
                TACTICAL ALERT: {alert.title} - {alert.message}
            </Message>
            <Dismiss onClick={() => setVisible(false)}>
                <X size={20} />
            </Dismiss>
        </Bar>
    ) : (
        <Bar active={visible}>
            <ShieldCheck size={20} color="#27AE60" />
            <Message style={{ color: '#7F8C8D' }}>
                SYSTEM STATUS: NOMINAL. ALL VECTORS SECURE.
            </Message>
        </Bar>
    );

    return <Root>{content}</Root>;
};

export default AlertTicker;
