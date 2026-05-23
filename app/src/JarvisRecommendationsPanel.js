import React from 'react';
import styled from 'styled-components';
import { Bot, ChevronRight, Zap } from 'lucide-react';

const Root = styled.div`
    display: flex;
    flex-direction: column;
    gap: 15px;
    height: 100%;
`;

const ScrollArea = styled.div`
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding-right: 5px;
    -webkit-overflow-scrolling: touch;

    &::-webkit-scrollbar { width: 4px; }
    &::-webkit-scrollbar-thumb { background: ${props => props.theme.colors.border}; border-radius: 2px; }
`;

const RecCard = styled.div`
    background: #fff;
    border: 1px solid ${props => props.theme.colors.border}44;
    border-radius: 15px;
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;

    &:hover {
        border-color: ${props => props.theme.colors.primary};
        box-shadow: 0 5px 15px rgba(0,0,0,0.03);
        transform: translateX(5px);
    }
`;

const RecInfo = styled.div`
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 5px;
`;

const RecTitle = styled.div`
    font-size: 0.9rem;
    font-weight: 800;
    color: ${props => props.theme.colors.primary};
    text-transform: uppercase;
    letter-spacing: 1px;
`;

const RecDesc = styled.div`
    font-size: 0.75rem;
    color: ${props => props.theme.colors.textSecondary};
    font-weight: 600;
    line-height: 1.4;
`;

const ExecuteBtn = styled.button`
    background: ${props => props.theme.colors.primary}11;
    color: ${props => props.theme.colors.primary};
    border: 1px solid ${props => props.theme.colors.primary}44;
    padding: 10px 15px;
    border-radius: 10px;
    font-size: 0.7rem;
    font-weight: 900;
    text-transform: uppercase;
    cursor: pointer;
    transition: 0.3s;
    min-height: 40px;

    &:hover {
        background: ${props => props.theme.colors.primary};
        color: #fff;
    }
`;

const JarvisRecommendationsPanel = ({ onExecute }) => {
    const recommendations = [
        {
            title: 'Scan WEBSVR01 for Shellshock',
            description: 'Asset "WEBSVR01" is running an old version of Apache. A Shellshock vulnerability scan is recommended.',
            command: 'nmap -sV -p 80 --script http-shellshock --script-args uri=/cgi-bin/test.cgi 192.168.1.101'
        },
        {
            title: 'Attempt EternalBlue on WIN10-DEV',
            description: 'Asset "WIN10-DEV" appears unpatched. MS17-010 is a high-probability vector.',
            command: `msfconsole -x "use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS 192.168.1.105; run"`
        },
        {
            title: 'Bluetooth Fast Pair Probe',
            description: 'Local spectral scan detected multiple GFPS devices. Attempt WhisperPair (CVE-2025-36911).',
            command: 'jarvis blue-probe --all'
        }
    ];

    return (
        <Root>
            <ScrollArea>
                {recommendations.map((rec, i) => (
                    <RecCard key={i}>
                        <Bot size={20} color="#00AAFF" style={{ flexShrink: 0 }} />
                        <RecInfo>
                            <RecTitle>{rec.title}</RecTitle>
                            <RecDesc>{rec.description}</RecDesc>
                        </RecInfo>
                        <ExecuteBtn onClick={() => onExecute(rec.command)}>
                            Execute
                        </ExecuteBtn>
                    </RecCard>
                ))}
            </ScrollArea>
        </Root>
    );
};

export default JarvisRecommendationsPanel;
