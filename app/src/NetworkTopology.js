import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { Share2, Server, Smartphone, Globe, ShieldCheck, Zap } from 'lucide-react';

const pulse = keyframes`
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.1); opacity: 0.7; }
    100% { transform: scale(1); opacity: 1; }
`;

const Root = styled.div`
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 30px;
    padding: 30px;
    color: ${props => props.theme.colors.text};
`;

const Header = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
`;

const TitleGroup = styled.div`
    display: flex;
    flex-direction: column;
    gap: 8px;
`;

const Title = styled.h2`
    font-size: 1.4rem;
    font-weight: 900;
    margin: 0;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: ${props => props.theme.colors.primary};
`;

const Subtitle = styled.p`
    font-size: 0.8rem;
    color: ${props => props.theme.colors.textSecondary};
    margin: 0;
    font-weight: 600;
    letter-spacing: 1px;
`;

const Viewport = styled.div`
    flex: 1;
    background: #fff;
    ${props => props.theme.effects.glass}
    border-radius: 30px;
    position: relative;
    overflow: hidden;
    box-shadow: ${props => props.theme.effects.shadow};
`;

const NodeContainer = styled.div`
    position: absolute;
    left: ${props => props.pos.x}px;
    top: ${props => props.pos.y}px;
    width: 100px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    cursor: grab;
    transform: translate(-50%, -50%);
    transition: transform 0.2s;
    z-index: 10;

    &:active {
        cursor: grabbing;
        transform: translate(-50%, -50%) scale(1.1);
    }
`;

const NodeIcon = styled.div`
    width: 65px;
    height: 65px;
    background: #fff;
    border: 3px solid ${props => props.color};
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05), 0 0 15px ${props => props.color}22;
    transition: 0.3s;
    
    ${props => props.status === 'warning' && css`
        animation: ${pulse} 2s infinite ease-in-out;
    `}

    svg {
        width: 30px;
        height: 30px;
    }
`;

const NodeLabel = styled.div`
    font-size: 0.7rem;
    font-weight: 800;
    color: ${props => props.theme.colors.textSecondary};
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 1px;
    background: rgba(255,255,255,0.8);
    padding: 4px 10px;
    border-radius: 8px;
    backdrop-filter: blur(5px);
`;

const Legend = styled.div`
    position: absolute;
    bottom: 30px;
    right: 30px;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid ${props => props.theme.colors.border};
    font-size: 0.7rem;
    display: flex;
    flex-direction: column;
    gap: 12px;
    box-shadow: ${props => props.theme.effects.shadow};
`;

const LegendItem = styled.div`
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 700;
    color: ${props => props.theme.colors.text};
    text-transform: uppercase;
    letter-spacing: 1px;
`;

const Dot = styled.div`
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: ${props => props.color};
    box-shadow: 0 0 10px ${props => props.color};
`;

const ActionButton = styled.button`
    background: #00AAFF;
    border: none;
    color: #fff;
    padding: 15px 30px;
    border-radius: 15px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 5px 15px rgba(0, 170, 255, 0.3);
    transition: 0.3s;
    min-height: 55px;

    &:hover {
        background: #0088CC;
        transform: translateY(-2px);
    }
`;

const NetworkTopology = () => {
    const [nodes, setNodes] = useState([
        { id: 'master', label: 'MASTER_UPLINK', type: 'core', pos: { x: 500, y: 350 }, status: 'active' },
        { id: 'c2', label: 'C2_REGISTRY', type: 'service', pos: { x: 500, y: 150 }, status: 'active' },
        { id: 'iot-1', label: 'NODE_ALPHA', type: 'iot', pos: { x: 250, y: 250 }, status: 'active' },
        { id: 'iot-2', label: 'NODE_BETA', type: 'iot', pos: { x: 750, y: 250 }, status: 'warning' },
        { id: 'mobile', label: 'MOBILE_HUB', type: 'endpoint', pos: { x: 500, y: 550 }, status: 'active' },
    ]);

    const connections = [
        { from: 'master', to: 'c2' },
        { from: 'master', to: 'iot-1' },
        { from: 'master', to: 'iot-2' },
        { from: 'master', to: 'mobile' },
        { from: 'c2', to: 'mobile' },
    ];

    const COLORS = {
        core: '#00AAFF',
        service: '#6366f1',
        iot: '#27AE60',
        endpoint: '#F39C12',
        warning: '#E74C3C',
        border: '#D1D9E6'
    };

    return (
        <Root>
            <Header>
                <TitleGroup>
                    <Title>Network Topology</Title>
                    <Subtitle>Real-time infrastructure mapping and route visualization.</Subtitle>
                </TitleGroup>
                <ActionButton onClick={() => console.log('Rescanning...')}>
                    <Zap size={20} /> Rescan Grid
                </ActionButton>
            </Header>

            <Viewport>
                <svg style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none' }}>
                    {connections.map((conn, i) => {
                        const fromNode = nodes.find(n => n.id === conn.from);
                        const toNode = nodes.find(n => n.id === conn.to);
                        return (
                            <line 
                                key={i}
                                x1={fromNode.pos.x} y1={fromNode.pos.y}
                                x2={toNode.pos.x} y2={toNode.pos.y}
                                stroke="#D1D9E6"
                                strokeWidth="3"
                                strokeDasharray="8,8"
                                opacity="0.6"
                            />
                        );
                    })}
                </svg>

                {nodes.map(node => (
                    <NodeContainer 
                        key={node.id}
                        pos={node.pos}
                    >
                        <NodeIcon 
                            color={node.status === 'warning' ? COLORS.warning : COLORS[node.type]}
                            status={node.status}
                        >
                            {node.type === 'core' && <ShieldCheck color={COLORS.core} />}
                            {node.type === 'service' && <Server color={COLORS.service} />}
                            {node.type === 'iot' && <Share2 color={COLORS.iot} />}
                            {node.type === 'endpoint' && <Smartphone color={COLORS.endpoint} />}
                        </NodeIcon>
                        <NodeLabel>{node.label}</NodeLabel>
                    </NodeContainer>
                ))}

                <Legend>
                    <LegendItem><Dot color={COLORS.core} /> CORE_IDENTITY</LegendItem>
                    <LegendItem><Dot color={COLORS.service} /> BACKEND_SERVICE</LegendItem>
                    <LegendItem><Dot color={COLORS.iot} /> IOT_VECTOR</LegendItem>
                    <LegendItem><Dot color={COLORS.warning} /> ALERT_STATE</LegendItem>
                </Legend>
            </Viewport>
        </Root>
    );
};

export default NetworkTopology;
