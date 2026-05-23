import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { Share2, Zap, Info, ShieldAlert } from 'lucide-react';

const fadeIn = keyframes`
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
`;

const Root = styled.div`
    padding: 30px;
    color: ${props => props.theme.colors.text};
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 30px;
    overflow-y: auto;
    /* Touchscreen scroll optimization */
    -webkit-overflow-scrolling: touch;
`;

const Header = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid ${props => props.theme.colors.border};
    padding-bottom: 20px;
    @media (max-width: 600px) {
        flex-direction: column;
        gap: 15px;
        align-items: flex-start;
    }
`;

const Title = styled.h2`
    margin: 0;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-size: 1.1rem;
    font-weight: 800;
    color: ${props => props.theme.colors.primary};
`;

const Grid = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
`;

const DeviceCard = styled.div`
    ${props => props.theme.effects.glass}
    background: ${props => props.theme.colors.glass};
    padding: 25px;
    border-radius: 20px;
    position: relative;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    animation: ${fadeIn} 0.5s ease-out backwards;
    animation-delay: ${props => props.index * 0.05}s;

    &:hover {
        transform: translateY(-5px);
        box-shadow: ${props => props.theme.effects.shadow};
        border-color: ${props => props.theme.colors.primary};
    }

    &:active {
        transform: scale(0.98);
    }
`;

const DeviceType = styled.div`
    font-size: 0.6rem;
    color: ${props => props.theme.colors.textSecondary};
    position: absolute;
    top: 15px;
    right: 20px;
    text-transform: uppercase;
    font-weight: 800;
    letter-spacing: 1px;
`;

const DeviceName = styled.div`
    font-size: 1.2rem;
    font-weight: 900;
    margin-bottom: 15px;
    color: ${props => props.theme.colors.text};
`;

const DeviceMeta = styled.div`
    font-size: 0.85rem;
    color: ${props => props.theme.colors.textSecondary};
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 8px;
`;

const ActionGroup = styled.div`
    margin-top: 25px;
    display: flex;
    gap: 12px;
`;

const IconButton = styled.button`
    background: ${props => props.primary ? props.theme.colors.primary : 'transparent'};
    color: ${props => props.primary ? '#fff' : props.theme.colors.primary};
    border: ${props => props.primary ? 'none' : `1px solid ${props.theme.colors.primary}`};
    padding: 15px;
    border-radius: 12px;
    cursor: pointer;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: 0.3s;
    /* Larger touch target */
    min-height: 55px;

    &:hover {
        opacity: 0.9;
        box-shadow: 0 0 15px ${props => props.theme.colors.glow};
    }

    &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
`;

const ScanButton = styled(IconButton)`
    width: auto;
    padding: 12px 25px;
    flex: none;
`;

const ErrorBanner = styled.div`
    background: ${props => props.theme.colors.error}11;
    border: 1px solid ${props => props.theme.colors.error}44;
    color: ${props => props.theme.colors.error};
    padding: 20px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    gap: 15px;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.8rem;
    letter-spacing: 1px;
`;

const EmptyState = styled.div`
    grid-column: 1/-1;
    text-align: center;
    padding: 80px 40px;
    border: 2px dashed ${props => props.theme.colors.border};
    border-radius: 20px;
    color: ${props => props.theme.colors.textSecondary};
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    opacity: 0.5;
`;

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
        const prompt = `analyze iot device: ${device.name} at ${device.addresses[0]} type ${device.type}. Properties: ${JSON.stringify(device.properties)}`;
        ipcRenderer.send('terminal.keystroke', `jarvis ${prompt}\r`);
        // We could use a more high-fidelity notification system here
    };

    return (
        <Root>
            <Header>
                <Title>SMART_VECTORS // IoT DISCOVERY</Title>
                <ScanButton 
                    primary 
                    onClick={scanNetwork}
                    disabled={loading}
                >
                    <Zap size={18} />
                    {loading ? 'SCANNING_GRID...' : 'SCAN_NETWORK'}
                </ScanButton>
            </Header>

            {error && (
                <ErrorBanner>
                    <ShieldAlert size={20} />
                    {error}
                </ErrorBanner>
            )}

            <div style={{ flex: 1 }}>
                <Grid>
                    {devices.map((dev, i) => (
                        <DeviceCard key={i} index={i}>
                            <DeviceType>{dev.type}</DeviceType>
                            <DeviceName>{dev.name.split('.')[0]}</DeviceName>
                            <DeviceMeta><Share2 size={14} /> {dev.addresses[0]}</DeviceMeta>
                            <DeviceMeta><Zap size={14} /> PORT: {dev.port}</DeviceMeta>
                            
                            <ActionGroup>
                                <IconButton 
                                    primary 
                                    onClick={() => engageDevice(dev)}
                                >
                                    AI_ENGAGE
                                </IconButton>
                                <IconButton 
                                    onClick={() => alert(`INTEL DATA:\n${JSON.stringify(dev.properties, null, 2)}`)}
                                >
                                    <Info size={16} />
                                    INTEL
                                </IconButton>
                            </ActionGroup>
                        </DeviceCard>
                    ))}
                    {devices.length === 0 && !loading && (
                        <EmptyState>
                            NO SMART VECTORS DETECTED IN LOCAL BROADCAST DOMAIN.
                        </EmptyState>
                    )}
                </Grid>
            </div>
        </Root>
    );
};

export default IoTDashboard;
