import React from 'react';
import styled from 'styled-components';
import { Scan, Bug, Lock, Zap, MousePointer2 } from 'lucide-react';

const Root = styled.div`
    display: flex;
    flex-direction: column;
    gap: 20px;
    height: 100%;
`;

const EmptyState = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1;
    color: ${props => props.theme.colors.textSecondary};
    opacity: 0.5;
    gap: 15px;
    text-transform: uppercase;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 2px;
`;

const TargetHeader = styled.div`
    font-size: 1rem;
    font-weight: 900;
    color: ${props => props.theme.colors.primary};
    padding-bottom: 15px;
    border-bottom: 1px solid ${props => props.theme.colors.border};
    text-transform: uppercase;
    letter-spacing: 2px;
`;

const ActionGrid = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
`;

const ActionButton = styled.button`
    background: #fff;
    border: 1px solid ${props => props.theme.colors.border};
    padding: 20px;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    min-height: 110px;

    &:hover {
        border-color: ${props => props.theme.colors.primary};
        transform: translateY(-5px);
        box-shadow: ${props => props.theme.effects.shadow};
    }

    &:active {
        transform: scale(0.95);
    }
`;

const ActionIcon = styled.div`
    color: ${props => props.theme.colors.primary};
`;

const ActionName = styled.div`
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: ${props => props.theme.colors.text};
`;

const ActionPanel = ({ selectedTarget, onExecute }) => {
    if (!selectedTarget) {
        return (
            <Root>
                <EmptyState>
                    <MousePointer2 size={40} />
                    NO TARGET ACQUIRED
                </EmptyState>
            </Root>
        );
    }
    
    const actions = [
        { name: 'Aggressive Scan', icon: <Scan size={24} />, command: `nmap -T4 -A -v ${selectedTarget}`},
        { name: 'Vuln Scan', icon: <Bug size={24} />, command: `nmap --script vuln ${selectedTarget}`},
        { name: 'Harden (Defensive)', icon: <Lock size={24} />, command: `ansible-playbook harden.yml --limit ${selectedTarget}`},
        { name: 'Exploit (MS17-010)', icon: <Zap size={24} />, command: `msfconsole -x "use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS ${selectedTarget}; run"`},
    ];

    return (
        <Root>
            <TargetHeader>ACTIVE_TARGET: {selectedTarget}</TargetHeader>
            <ActionGrid>
                {actions.map(action => (
                    <ActionButton key={action.name} onClick={() => onExecute(action.command)}>
                        <ActionIcon>{action.icon}</ActionIcon>
                        <ActionName>{action.name}</ActionName>
                    </ActionButton>
                ))}
            </ActionGrid>
        </Root>
    );
};

export default ActionPanel;
