import React, { useState, useEffect } from 'react';
import styled, { keyframes, css } from 'styled-components';
import { CheckCircle2, RefreshCw, AlertCircle, Cpu, HardDrive, ShieldCheck, Activity } from 'lucide-react';

const spin = keyframes`
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
`;

const Root = styled.div`
    display: flex;
    flex-direction: column;
    gap: 20px;
    height: 100%;
`;

const Grid = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 15px;
`;

const StatCard = styled.div`
    background: rgba(255, 255, 255, 0.4);
    border: 1px solid ${props => props.theme.colors.border}44;
    padding: 15px;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    transition: 0.3s;

    &:hover {
        background: #fff;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
`;

const StatLabel = styled.div`
    font-size: 0.65rem;
    font-weight: 800;
    color: ${props => props.theme.colors.textSecondary};
    text-transform: uppercase;
    letter-spacing: 1px;
`;

const StatValue = styled.div`
    font-size: 0.85rem;
    font-weight: 900;
    color: ${props => props.color || props.theme.colors.text};
    display: flex;
    align-items: center;
    gap: 6px;

    svg {
        width: 14px;
        height: 14px;
        ${props => props.spinning && css`
            animation: ${spin} 2s linear infinite;
        `}
    }
`;

const OverallStatus = styled.div`
    background: ${props => props.status === 'NOMINAL' ? props.theme.colors.success : props.theme.colors.warning}11;
    border: 1px solid ${props => props.status === 'NOMINAL' ? props.theme.colors.success : props.theme.colors.warning}44;
    color: ${props => props.status === 'NOMINAL' ? props.theme.colors.success : props.theme.colors.warning};
    padding: 15px 20px;
    border-radius: 12px;
    font-weight: 900;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    display: flex;
    align-items: center;
    justify-content: space-between;
`;

const ipcRenderer = window.electronAPI?.ipcRenderer;

const SystemStatusPanel = () => {
    const [status, setStatus] = useState({
        uplink: { status: 'CONNECTING' },
        database: { status: 'CONNECTING' },
        scanner: { status: 'UNKNOWN' },
        exploitEngine: { status: 'UNKNOWN' },
        overall: 'INITIALIZING'
    });

    useEffect(() => {
        if (!ipcRenderer) return;
        const getStatus = async () => {
            try {
                const newStatus = await ipcRenderer.invoke('system.getDetailedStatus');
                if (newStatus) setStatus(newStatus);
            } catch (e) {
                console.error('STATUS_FETCH_FAIL', e);
            }
        };
        const interval = setInterval(getStatus, 2500);
        getStatus();
        return () => clearInterval(interval);
    }, []);

    const getStatusProps = (stat) => {
        switch (stat) {
            case 'SECURE': case 'SYNCED': case 'IDLE': case 'CONNECTED': case 'NOMINAL': case 'ONLINE':
                return { color: '#27AE60', icon: <CheckCircle2 /> };
            case 'CONNECTING': case 'SYNCING': case 'SCANNING': case 'INITIALIZING':
                 return { color: '#00AAFF', icon: <RefreshCw />, spinning: true };
            default:
                return { color: '#E74C3C', icon: <AlertCircle /> };
        }
    };

    return (
        <Root>
            <OverallStatus status={status.overall === 'ONLINE' ? 'NOMINAL' : 'INITIALIZING'}>
                SYSTEM_STATE: {status.overall}
                {getStatusProps(status.overall).icon}
            </OverallStatus>
            
            <Grid>
                {[
                    { label: 'UPLINK (TOR)', key: 'uplink' },
                    { label: 'EXPLOIT DB', key: 'database' },
                    { label: 'NMAP CORE', key: 'scanner' },
                    { label: 'ATTACK ENG', key: 'exploitEngine' }
                ].map(item => {
                    const props = getStatusProps(status[item.key]?.status || 'UNKNOWN');
                    return (
                        <StatCard key={item.key}>
                            <StatLabel>{item.label}</StatLabel>
                            <StatValue color={props.color} spinning={props.spinning}>
                                {props.icon}
                                {status[item.key]?.status || 'UNKNOWN'}
                            </StatValue>
                        </StatCard>
                    );
                })}
            </Grid>
        </Root>
    );
};

export default SystemStatusPanel;
