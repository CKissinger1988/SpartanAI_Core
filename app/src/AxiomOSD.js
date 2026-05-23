import React from 'react';
import styled from 'styled-components';
import { Activity, ShieldCheck, Cpu, Database, AlertCircle } from 'lucide-react';

const Root = styled.div`
    padding: 30px;
    background-color: #E8EDF2;
    background-image: radial-gradient(circle at 50% 50%, #FFFFFF 0%, #E8EDF2 100%);
    color: #2C3E50;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 30px;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
`;

const Header = styled.h1`
    font-size: 1.4rem;
    font-weight: 900;
    text-align: center;
    color: ${props => props.theme.colors.primary};
    letter-spacing: 6px;
    text-transform: uppercase;
    margin: 0;
`;

const Grid = styled.div`
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
    @media (max-width: 900px) {
        grid-template-columns: 1fr;
    }
`;

const DiagnosticCard = styled.div`
    ${props => props.theme.effects.glass}
    background: ${props => props.theme.colors.glass};
    padding: 25px;
    border-radius: 25px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    text-align: center;
    box-shadow: ${props => props.theme.effects.shadow};
`;

const Label = styled.div`
    font-size: 0.75rem;
    font-weight: 800;
    color: ${props => props.theme.colors.textSecondary};
    text-transform: uppercase;
    letter-spacing: 2px;
`;

const Value = styled.div`
    font-size: 2.2rem;
    font-weight: 900;
    color: ${props => props.theme.colors.primary};
`;

const LogCard = styled.div`
    ${props => props.theme.effects.glass}
    background: #fff;
    padding: 30px;
    border-radius: 30px;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
    box-shadow: ${props => props.theme.effects.shadow};
`;

const LogList = styled.div`
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
`;

const LogItem = styled.div`
    display: flex;
    gap: 15px;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 10px;
    border-bottom: 1px solid ${props => props.theme.colors.border}44;

    .timestamp {
        color: ${props => props.theme.colors.primary};
        font-family: 'Fira Code', monospace;
        font-weight: 800;
    }
`;

const AxiomOSD = ({ status, cognitive_state, swarm_logs }) => {
    return (
        <Root>
            <Header>[ MASTER COMMAND DIAGNOSTIC ]</Header>
            <Grid>
                <DiagnosticCard>
                    <Label>Neural Engine Health</Label>
                    <Value>{status.confidence}%</Value>
                    <div style={{ fontSize: '0.65rem', fontWeight: 800, color: '#27AE60' }}>PATTERN CONFIDENCE: OPTIMAL</div>
                </DiagnosticCard>
                <DiagnosticCard>
                    <Label>Hive-Mind Swarm</Label>
                    <Value>{swarm_logs.active_agents}</Value>
                    <div style={{ fontSize: '0.65rem', fontWeight: 800, color: '#00AAFF' }}>ACTIVE SPECIALISTS ONLINE</div>
                </DiagnosticCard>
                <DiagnosticCard>
                    <Label>Safety Verificator</Label>
                    <ShieldCheck size={40} color="#27AE60" />
                    <div style={{ fontSize: '0.75rem', fontWeight: 900, color: '#27AE60', textTransform: 'uppercase' }}>Logic Proofs: Verified</div>
                </DiagnosticCard>
            </Grid>
            <LogCard>
                <Label>Cognitive Operation Logs</Label>
                <LogList>
                    {cognitive_state.map((item, index) => (
                        <LogItem key={index}>
                            <span className="timestamp">[{item.timestamp}]</span>
                            <span>{item.thought}</span>
                        </LogItem>
                    ))}
                </LogList>
            </LogCard>
        </Root>
    );
};

export default AxiomOSD;
