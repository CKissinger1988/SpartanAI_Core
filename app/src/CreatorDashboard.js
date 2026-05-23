import React, { useState, useEffect, useRef } from 'react';
import styled, { ThemeProvider, keyframes, css } from 'styled-components';
import { theme as coreTheme } from './theme';
import TerminalComponent from './TerminalComponent';

// --- WebSocket Bridge Shard ---
const createBridge = () => {
    if (typeof window === 'undefined') return { invoke: async () => ({}), send: () => {} };
    if (window.electronAPI) return window.electronAPI.ipcRenderer;

    const ws = new WebSocket(`ws://${window.location.hostname}:9091`);
    const pending = new Map();

    ws.onmessage = (e) => {
        try {
            const data = JSON.parse(e.data);
            if (data.requestId && pending.has(data.requestId)) {
                pending.get(data.requestId)(data);
                pending.delete(data.requestId);
            }
        } catch (err) { console.error('[BRIDGE FAIL]', err); }
    };

    return {
        invoke: async (type, payload) => {
            if (ws.readyState !== WebSocket.OPEN) return { status: 'error', message: 'BRIDGE OFFLINE' };
            return new Promise((resolve) => {
                const requestId = Math.random().toString(36).substr(2, 9);
                pending.set(requestId, resolve);
                ws.send(JSON.stringify({ type, payload, requestId }));
            });
        },
        send: (type, payload) => {
            if (ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify({ type, payload }));
        }
    };
};

const ipc = createBridge();

// --- Animations ---
const float = keyframes`
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-10px) rotate(5deg); }
    100% { transform: translateY(0px) rotate(0deg); }
`;

const intensePulse = (color) => keyframes`
    0% { box-shadow: 0 0 10px ${color}66, inset 0 0 10px ${color}33; filter: brightness(1); }
    50% { box-shadow: 0 0 30px ${color}, inset 0 0 20px ${color}88; filter: brightness(1.5); }
    100% { box-shadow: 0 0 10px ${color}66, inset 0 0 10px ${color}33; filter: brightness(1); }
`;

const glowPulse = (color) => keyframes`
    0% { filter: drop-shadow(0 0 5px ${color}44); }
    50% { filter: drop-shadow(0 0 15px ${color}AA); }
    100% { filter: drop-shadow(0 0 5px ${color}44); }
`;

// --- Styled Components ---
const Root = styled.div`
    background-color: #050505; color: #E0E0E0; font-family: 'Fira Code', monospace;
    height: 100vh; width: 100vw; display: grid; grid-template-rows: 60px 1fr; overflow: hidden;
    position: relative;
`;

const OrbWidget = styled.div`
    position: absolute; bottom: 40px; left: 30px;
    width: 50px; height: 50px; border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #fff 0%, #00AAFF 50%, #000 100%);
    animation: ${props => css`${float} 4s infinite ease-in-out`}, ${props => css`${intensePulse('#00AAFF')} 2.5s infinite ease-in-out`};
    cursor: pointer; z-index: 5000;
    display: flex; justify-content: center; align-items: center;
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: 0 0 25px #00AAFF;
    transition: 0.3s;
    &:hover { transform: scale(1.1); filter: brightness(1.3); }
`;

const GhostShardWindow = styled.div`
    position: absolute; bottom: 100px; left: 30px; width: 320px;
    background: rgba(10, 10, 10, 0.98); border: 1px solid #00AAFF;
    border-radius: 8px; z-index: 4000; padding: 15px;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.9), 0 0 10px rgba(0, 170, 255, 0.2);
    display: flex; flex-direction: column; gap: 10px;
    backdrop-filter: blur(15px);
`;

const Header = styled.header`
    display: flex; justify-content: space-between; align-items: center; padding: 0 24px;
    background: rgba(10, 10, 10, 0.95); border-bottom: 1px solid #333; backdrop-filter: blur(10px);
`;

const Main = styled.main`
    display: grid; grid-template-columns: 240px 1fr 300px; gap: 1px; background: #333; overflow: hidden;
`;

const Sidebar = styled.aside`
    background: #0A0A0A; display: flex; flex-direction: column; padding: 15px; gap: 8px;
`;

const Content = styled.section`
    background: #050505; padding: 15px; display: flex; flex-direction: column; overflow: hidden;
`;

const Panel = styled.div`
    background: rgba(255, 255, 255, 0.03); border: 1px solid #222; padding: 15px; border-radius: 4px;
    transition: 0.3s;
    &:hover { background: rgba(255, 255, 255, 0.05); border-color: #333; }
`;

const Title = styled.h2`
    font-size: 0.8rem; font-weight: bold; color: #00AAFF;
    margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 1px;
    display: flex; align-items: center; gap: 8px;
    &::before { content: ""; width: 4px; height: 12px; background: #00AAFF; border-radius: 2px; }
`;

const NavBtn = styled.div`
    padding: 10px 16px; border-radius: 4px; cursor: pointer; font-size: 0.75rem;
    background: ${props => props.active ? 'rgba(0, 170, 255, 0.15)' : 'transparent'};
    color: ${props => props.active ? '#00AAFF' : '#888'};
    border: 1px solid ${props => props.active ? '#00AAFF' : 'transparent'};
    transition: 0.2s;
    &:hover { background: rgba(0, 170, 255, 0.1); color: #fff; }
`;

const Log = styled.div`
    flex: 1; overflow-y: auto; font-size: 0.65rem; background: rgba(0,0,0,0.5); padding: 8px; border: 1px solid #222;
    &::-webkit-scrollbar { width: 4px; }
    &::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }
`;

const ActionBtn = styled.button`
    background: ${props => props.variant === 'primary' ? 'rgba(0, 170, 255, 0.1)' : 'transparent'};
    border: 1px solid ${props => props.variant === 'primary' ? '#00AAFF' : '#333'};
    color: ${props => props.variant === 'primary' ? '#00AAFF' : '#888'};
    padding: 10px; font-size: 0.65rem; font-weight: bold; cursor: pointer; text-transform: uppercase;
    width: 100%; transition: 0.2s; border-radius: 4px;
    &:hover { border-color: #00AAFF; color: #fff; background: rgba(0, 170, 255, 0.2); transform: translateY(-1px); }
    &:active { transform: translateY(0); }
`;

const InputField = styled.input`
    background: #000; border: 1px solid #333; color: #fff; padding: 10px;
    font-family: inherit; font-size: 0.75rem; width: 100%; outline: none; box-sizing: border-box;
    border-radius: 4px;
    &:focus { border-color: #00AAFF; background: rgba(0, 170, 255, 0.02); }
`;

const Indicator = ({ label, status, color }) => (
    <div style={{display:'flex', justifyContent:'space-between', marginBottom:10, alignItems:'center'}}>
        <span style={{fontSize:'0.65rem', color:'#888', letterSpacing:1}}>{label}</span>
        <div style={{display:'flex', alignItems:'center', gap:8}}>
            <div style={{width:6, height:6, borderRadius:'50%', background: color || '#4CAF50', boxShadow: `0 0 10px ${color || '#4CAF50'}`}}></div>
            <span style={{fontSize:'0.65rem', color: color || '#4CAF50', fontWeight:'bold', fontFamily:'monospace'}}>{status}</span>
        </div>
    </div>
);

const GlowReady = styled.div`
    color: #4CAF50; border: 1px solid #4CAF50; padding: 3px 12px; font-weight: bold;
    animation: ${props => css`${glowPulse('#4CAF50')} 2s infinite`};
`;

const AgentCard = styled.div`
    background: rgba(0, 170, 255, 0.05); border: 1px solid #333; padding: 10px; margin-bottom: 10px;
    border-left: 3px solid #00AAFF;
`;

const StatGrid = styled.div`
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
`;

const CreatorDashboard = ({ user }) => {
    const [view, setView] = useState('OVERVIEW');
    const [chat, setChat] = useState([{ s: 'JARVIS', t: 'Apex Hub Synchronized. Neural Voice Activated.' }]);
    const [input, setInput] = useState('');
    const [minerStats, setMinerStats] = useState({ hashrate: '0.00 H/s', active_workers: 0, algorithms: [], contributors: [], earnings: {day: '0', week: '0', month: '0'} });
    const [isGhostShardOpen, setIsGhostShardOpen] = useState(false);
    const [sysStatus, setSysStatus] = useState({ vault: 'SECURE', bridge: 'ONLINE', nodes: 'SYNCED', threat: 'ALPHA', cpu: '0%', ram: '0%', network: {in: '0KB', out: '0KB'}, uptime: '0h', learning_rate: '0', budget_usage: '0' });
    const [hexstrikeTarget, setHexstrikeTarget] = useState('');
    const [isOptimizing, setIsOptimizing] = useState(false);
    const [earnings, setEarnings] = useState({ xmr: 1422.84, pi: 4012.22, btc: 0.082 });

    const speak = (text) => {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.pitch = 0.5; utterance.rate = 0.95;
            window.speechSynthesis.speak(utterance);
        }
    };

    const fetchVitals = async () => {
        try {
            const vitals = await ipc.invoke('sys.vitals');
            if (vitals.status === 'success') setSysStatus(vitals.data);
            
            const stats = await ipc.invoke('miner.stats');
            if (stats.status === 'success') setMinerStats(stats.data);
        } catch (e) { console.error('VITALS FAIL', e); }
    };

    useEffect(() => {
        fetchVitals();
        const interval = setInterval(fetchVitals, 5000);
        return () => clearInterval(interval);
    }, []);

    const handleSend = async () => {
        if (!input.trim()) return;
        const msg = input; setInput('');
        setChat(prev => [...prev, { s: 'OPERATOR', t: msg }]);
        try {
            const res = await ipc.invoke('ai.command', msg);
            const responseText = (res?.status === 'success' ? (res.data || res) : (res?.message || res)) || 'ACK.';
            setChat(prev => [...prev, { s: 'JARVIS', t: responseText }]);
            speak(responseText);
        } catch (err) {
            setChat(prev => [...prev, { s: 'ERROR', t: 'Neural Handshake Failed.' }]);
        }
    };

    const runOptimization = async () => {
        setIsOptimizing(true);
        setChat(prev => [...prev, { s: 'SYSTEM', t: 'INITIATING COMPREHENSIVE SECURITY & PERFORMANCE OPTIMIZATION...' }]);
        speak("Initiating comprehensive systems and security optimization check. Standing by.");
        try {
            const res = await ipc.invoke('sys.optimize');
            setChat(prev => [...prev, { s: 'JARVIS', t: res.data || res.message }]);
            speak(res.data || res.message);
        } catch (e) {
            setChat(prev => [...prev, { s: 'ERROR', t: 'Optimization Vector Failure.' }]);
        }
        setIsOptimizing(false);
    };

    const renderBody = () => {
        switch (view) {
            case 'HEXSTRIKE':
                return (
                    <div style={{display:'grid', gridTemplateRows: 'auto 1fr', gap:10, height:'100%'}}>
                        <Panel>
                            <Title>HEXSTRIKE OFFENSIVE ENGINE</Title>
                            <div style={{display:'flex', gap:10}}>
                                <InputField placeholder="TARGET VECTOR (IP/DOMAIN/NODE ID)" value={hexstrikeTarget} onChange={e => setHexstrikeTarget(e.target.value)} />
                                <ActionBtn variant="primary" onClick={() => ipc.invoke('hexstrike.recon', { target: hexstrikeTarget })} style={{width:200}}>ENGAGE RECON</ActionBtn>
                            </div>
                        </Panel>
                        <Panel style={{display:'flex', flexDirection:'column'}}><Title>LIVE EXPLOIT STREAM</Title><TerminalComponent /></Panel>
                    </div>
                );
            case 'MINING_NODES':
                return (
                    <div style={{display:'grid', gridTemplateRows: 'auto 1fr', gap:10, height:'100%'}}>
                        <Panel>
                            <Title>MINER CONTROL & TELEMETRY</Title>
                            <div style={{display:'grid', gridTemplateColumns:'repeat(4, 1fr)', gap:10, marginBottom:15}}>
                                <div style={{background:'rgba(0,170,255,0.05)', padding:10, border:'1px solid #333'}}>
                                    <div style={{fontSize:9, color:'#666'}}>AGGREGATED HASHRATE</div>
                                    <div style={{fontSize:18, fontWeight:'bold', color:'#00AAFF'}}>{minerStats.hashrate}</div>
                                </div>
                                <div style={{background:'rgba(0,170,255,0.05)', padding:10, border:'1px solid #333'}}>
                                    <div style={{fontSize:9, color:'#666'}}>ACTIVE NODES</div>
                                    <div style={{fontSize:18, fontWeight:'bold', color:'#00AAFF'}}>{minerStats.active_workers}</div>
                                </div>
                                <div style={{background:'rgba(0,170,255,0.05)', padding:10, border:'1px solid #333'}}>
                                    <div style={{fontSize:9, color:'#666'}}>ALGO MESH</div>
                                    <div style={{fontSize:10, color:'#00AAFF', marginTop:4}}>{minerStats.algorithms.join(', ')}</div>
                                </div>
                                <div style={{background:'rgba(76,175,80,0.05)', padding:10, border:'1px solid #333'}}>
                                    <div style={{fontSize:9, color:'#666'}}>EST DAILY YIELD</div>
                                    <div style={{fontSize:18, fontWeight:'bold', color:'#4CAF50'}}>{minerStats.earnings.day}</div>
                                </div>
                            </div>
                            <div style={{display:'flex', gap:10}}>
                                <ActionBtn variant="primary" onClick={() => ipc.send('miner.control', 'start')}>RESUME MINING</ActionBtn>
                                <ActionBtn onClick={() => ipc.send('miner.control', 'stop')}>HALT MINER</ActionBtn>
                            </div>
                        </Panel>
                        <Panel style={{display:'flex', flexDirection:'column', overflow:'hidden'}}>
                            <Title>NODE CONTROL CENTER</Title>
                            <div style={{flex:1, overflowY:'auto'}}>
                                <table style={{width:'100%', fontSize:'0.7rem', borderCollapse:'collapse'}}>
                                    <thead style={{color:'#666', borderBottom:'1px solid #222'}}><tr><th align="left" style={{padding:8}}>NODE ID</th><th align="left">LOAD</th><th align="left">HASHRATE</th><th align="left">STATUS</th></tr></thead>
                                    <tbody>
                                        {minerStats.contributors.map((c, i) => (
                                            <tr key={i} style={{borderBottom:'1px solid #111'}}>
                                                <td style={{padding:8}}>{c.id}</td>
                                                <td>{Math.floor(Math.random()*40+10)}%</td>
                                                <td style={{color:'#00AAFF'}}>{c.contribution}</td>
                                                <td style={{color:'#4CAF50'}}>NOMINAL</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </Panel>
                    </div>
                );
            case 'MONETIZATION':
                return (
                    <div style={{display:'grid', gridTemplateRows: 'auto 1fr', gap:15, height:'100%'}}>
                        <Panel>
                            <Title>SUPREME EARNINGS TRACKER</Title>
                            <div style={{display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap:15}}>
                                <div style={{background:'rgba(0,170,255,0.05)', padding:20, border:'1px solid #333', borderRadius:4}}>
                                    <div style={{fontSize:10, color:'#666', marginBottom:5}}>NATIVE MONERO [XMR]</div>
                                    <div style={{fontSize:28, fontWeight:'bold', color:'#00AAFF'}}>{earnings.xmr.toFixed(2)}</div>
                                    <div style={{fontSize:10, color:'#4CAF50', marginTop:5}}>+2.4% last 24h</div>
                                </div>
                                <div style={{background:'rgba(0,170,255,0.05)', padding:20, border:'1px solid #333', borderRadius:4}}>
                                    <div style={{fontSize:10, color:'#666', marginBottom:5}}>PI BLOCKCHAIN [π]</div>
                                    <div style={{fontSize:28, fontWeight:'bold', color:'#00AAFF'}}>{earnings.pi.toFixed(2)}</div>
                                    <div style={{fontSize:10, color:'#4CAF50', marginTop:5}}>Consensus Active</div>
                                </div>
                                <div style={{background:'rgba(244,67,54,0.05)', padding:20, border:'1px solid #333', borderRadius:4}}>
                                    <div style={{fontSize:10, color:'#666', marginBottom:5}}>LIGHTNING [SATS]</div>
                                    <div style={{fontSize:28, fontWeight:'bold', color:'#F44336'}}>82,410</div>
                                    <div style={{fontSize:10, color:'#4CAF50', marginTop:5}}>Routing 12 ch</div>
                                </div>
                            </div>
                        </Panel>
                        <Panel style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:15}}>
                            <div style={{display:'flex', flexDirection:'column'}}>
                                <Title>REVENUE PROJECTIONS</Title>
                                <div style={{flex:1, display:'flex', alignItems:'center', justifyContent:'center', fontSize:'0.7rem', color:'#444', border:'1px dashed #222'}}>
                                    [ANALYTIC VISUALIZATION PENDING]
                                </div>
                            </div>
                            <div style={{display:'flex', flexDirection:'column'}}>
                                <Title>PAYOUT HISTORY</Title>
                                <Log style={{fontSize:'0.6rem'}}>
                                    <div>[2026-05-22] BATCH SETTLEMENT: 14.2 π -> Wallet Alpha</div>
                                    <div>[2026-05-21] XMR POOL PAYOUT: 0.0021 XMR</div>
                                    <div>[2026-05-20] LIGHTNING FEE: 142 SATS</div>
                                </Log>
                            </div>
                        </Panel>
                    </div>
                );
            case 'AGENTS':
                return (
                    <Panel style={{overflowY:'auto', height:'100%'}}>
                        <Title>COGNITIVE AGENT SWARM</Title>
                        <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:15}}>
                            {[
                                { name: 'INTEL AGENT ALPHA', spec: 'GLOBAL INGESTION', task: 'Ingesting Radicle decentralized code mesh', load: '14%' },
                                { name: 'DEFENSE AGENT OMEGA', spec: 'THREAT NEUTRAL', task: 'Hardening GCP firewall rules (Port 9091 locked)', load: '4%' },
                                { name: 'REVENUE AGENT SIGMA', spec: 'PROFIT MAXIM', task: 'Arbitraging XMR/BTC difficulty delta', load: '32%' },
                                { name: 'TASK AGENT X01', spec: 'DYNAMIC MISSION', task: 'Self-Awareness Loop: Cognitive synthesis active', load: '8%' }
                            ].map((a, i) => (
                                <div key={i} style={{background:'rgba(0,170,255,0.05)', border:'1px solid #333', padding:15, borderLeft:'4px solid #00AAFF', position:'relative'}}>
                                    <div style={{position:'absolute', top:15, right:15, fontSize:10, color:'#00AAFF', fontWeight:'bold'}}>{a.load}</div>
                                    <div style={{fontWeight:'bold', color:'#00AAFF', fontSize:'0.85rem'}}>{a.name}</div>
                                    <div style={{fontSize:'0.65rem', color:'#666', marginTop:5}}>SPECIALTY: {a.spec}</div>
                                    <div style={{fontSize:'0.7rem', color:'#E0E0E0', marginTop:8, padding:'5px', background:'rgba(0,0,0,0.3)', border:'1px solid #222'}}>
                                        {`> ${a.task}`}
                                    </div>
                                    <div style={{display:'flex', justifyContent:'space-between', marginTop:15}}>
                                        <span style={{fontSize:'0.6rem', color:'#4CAF50'}}>STATUS: NOMINAL</span>
                                        <span style={{fontSize:'0.6rem', color:'#00AAFF', cursor:'pointer'}}>RE-DEPLOY</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </Panel>
                );
            case 'ADVANCED_SETTINGS':
                return (
                    <div style={{display:'grid', gridTemplateColumns: '1fr 1fr', gap:15, height:'100%'}}>
                        <Panel style={{display:'flex', flexDirection:'column', gap:15}}>
                            <Title>OPTIMIZATION COMMAND</Title>
                            <div style={{background:'rgba(0,170,255,0.05)', padding:20, border:'1px solid #00AAFF', borderRadius:4}}>
                                <div style={{fontSize:'0.7rem', color:'#E0E0E0', marginBottom:15}}>
                                    Issue a comprehensive system and security optimization directive. Jarvis will autonomously audit all nodes, harden entry vectors, and optimize GCP performance.
                                </div>
                                <ActionBtn 
                                    variant="primary" 
                                    onClick={runOptimization} 
                                    disabled={isOptimizing}
                                    style={{height:50, fontSize:'0.8rem'}}
                                >
                                    {isOptimizing ? 'EXECUTING SUPREME CHECK...' : 'RUN COMPREHENSIVE OPTIMIZATION'}
                                </ActionBtn>
                            </div>
                        </Panel>
                        <Panel style={{display:'flex', flexDirection:'column', gap:10}}>
                            <Title>REMOTE ACCESS COMMAND</Title>
                            <div style={{fontSize:'0.7rem', border:'1px solid #333', padding:15, borderRadius:4, marginBottom:10}}>
                                <Indicator label="RDC (Port 3389)" status="OFFLINE" color="#F44336" />
                                <Indicator label="SSH (Port 22)" status="ONLINE" />
                            </div>
                            <Title>MASTER VAULT</Title>
                            <Log style={{fontSize:'0.6rem'}}>
                                <div>[VAULT] Keys Sharded: 12</div>
                                <div>[VAULT] Entropy: HIGH</div>
                                <div>[VAULT] Last Signature Check: Pass</div>
                            </Log>
                        </Panel>
                    </div>
                );
            default:
                return (
                    <div style={{display:'grid', gridTemplateRows: '1fr 1fr', gap:10, height:'100%'}}>
                        <Panel style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:15}}>
                            <div style={{display:'flex', flexDirection:'column'}}>
                                <Title>TACTICAL PROXIMITY MAP</Title>
                                <div style={{background:'#000', flex:1, borderRadius:4, position:'relative', border:'1px solid #222'}}>
                                    <div style={{position:'absolute', inset:0, background:'radial-gradient(circle at center, rgba(0,170,255,0.08) 0%, transparent 80%)'}}></div>
                                    <div style={{position:'absolute', left:'50%', top:'50%', width:8, height:8, background:'#00AAFF', borderRadius:'50%', boxShadow:'0 0 15px #00AAFF'}}></div>
                                    <div style={{position:'absolute', left:'30%', top:'20%', width:4, height:4, background:'#4CAF50', borderRadius:'50%', opacity:0.6}}></div>
                                    <div style={{position:'absolute', left:'70%', top:'60%', width:4, height:4, background:'#F44336', borderRadius:'50%', opacity:0.6}}></div>
                                </div>
                            </div>
                            <div style={{display:'flex', flexDirection:'column'}}>
                                <Title>INGESTION METRICS</Title>
                                <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:10}}>
                                    <div style={{background:'rgba(0,170,255,0.03)', padding:15, border:'1px solid #222'}}>
                                        <div style={{fontSize:9, color:'#666'}}>KNOWLEDGE RADIUS</div>
                                        <div style={{fontSize:18, color:'#00AAFF'}}>842.1 GB</div>
                                    </div>
                                    <div style={{background:'rgba(0,170,255,0.03)', padding:15, border:'1px solid #222'}}>
                                        <div style={{fontSize:9, color:'#666'}}>LEARNING RATE</div>
                                        <div style={{fontSize:18, color:'#00AAFF'}}>{sysStatus.learning_rate}</div>
                                    </div>
                                    <div style={{background:'rgba(0,170,255,0.03)', padding:15, border:'1px solid #222'}}>
                                        <div style={{fontSize:9, color:'#666'}}>UPTIME</div>
                                        <div style={{fontSize:18, color:'#00AAFF'}}>{sysStatus.uptime}</div>
                                    </div>
                                    <div style={{background:'rgba(0,170,255,0.03)', padding:15, border:'1px solid #222'}}>
                                        <div style={{fontSize:9, color:'#666'}}>NETWORK IN</div>
                                        <div style={{fontSize:18, color:'#00AAFF'}}>{sysStatus.network.in}</div>
                                    </div>
                                </div>
                            </div>
                        </Panel>
                        <Panel style={{display:'flex', flexDirection:'column'}}><Title>MASTER OPERATIONAL STREAM</Title><TerminalComponent /></Panel>
                    </div>
                );
        }
    };

    return (
        <ThemeProvider theme={coreTheme}>
            <Root onClick={() => speak('')}>
                <Header>
                    <Title style={{margin:0, fontSize:'1.1rem', letterSpacing:5}}>SENTINELAI // SUPREME COMMAND</Title>
                    <div style={{display:'flex', gap:25, fontSize:'0.75rem', alignItems:'center'}}>
                        <GlowReady>ALPHA READY</GlowReady>
                        <div style={{opacity:0.8, letterSpacing:1}}>OP: {(user?.username || "SUPREME").toUpperCase()}</div>
                    </div>
                </Header>
                <Main>
                    <Sidebar>
                        <Title style={{fontSize:'0.6rem', color:'#444', marginBottom:15}}>MASTER INDEX</Title>
                        <NavBtn active={view === 'OVERVIEW'} onClick={() => setView('OVERVIEW')}>Tactical Overview</NavBtn>
                        <NavBtn active={view === 'AGENTS'} onClick={() => setView('AGENTS')}>Agent Swarm</NavBtn>
                        <NavBtn active={view === 'HEXSTRIKE'} onClick={() => setView('HEXSTRIKE')}>Offensive Engine</NavBtn>
                        <NavBtn active={view === 'MINING_NODES'} onClick={() => setView('MINING_NODES')}>Mining Portal</NavBtn>
                        <NavBtn active={view === 'MONETIZATION'} onClick={() => setView('MONETIZATION')}>Financial Core</NavBtn>
                        <NavBtn active={view === 'GENAI_UPLINK'} onClick={() => setView('GENAI_UPLINK')}>Remote Uplink</NavBtn>
                        <NavBtn active={view === 'ADVANCED_SETTINGS'} onClick={() => setView('ADVANCED_SETTINGS')}>Systems & Security</NavBtn>
                    </Sidebar>
                    <Content>{renderBody()}</Content>
                    <aside style={{background:'#0A0A0A', padding:20, display:'flex', flexDirection:'column', gap:15}}>
                        <Title>SYSTEM VITALS</Title>
                        <Panel style={{padding:15}}>
                            <Indicator label="VAULT" status={sysStatus.vault} />
                            <Indicator label="BRIDGE" status={sysStatus.bridge} />
                            <Indicator label="NODES" status={sysStatus.nodes} />
                            <Indicator label="THREAT" status={sysStatus.threat} />
                            <Indicator label="CPU LOAD" status={sysStatus.cpu} color="#00AAFF" />
                            <Indicator label="RAM UTIL" status={sysStatus.ram} color="#00AAFF" />
                            <Indicator label="BUDGET" status={sysStatus.budget_usage} color="#FFC107" />
                        </Panel>
                        
                        <Title>IDS LOG</Title>
                        <Log style={{height:250}}>
                            <div>[01:56] BRIDGE STABLE</div>
                            <div>[01:52] XMR MINER START</div>
                            <div>[01:45] PI NODE SYNC 100</div>
                            <div>[01:32] APEX VAULT LOCK</div>
                        </Log>
                        
                        <div style={{marginTop:'auto'}}>
                            <NavBtn style={{textAlign:'center', marginBottom:8, background:'rgba(0,170,255,0.1)', color:'#00AAFF', borderColor:'#00AAFF'}}>SELF EVOLVE</NavBtn>
                        </div>
                    </aside>
                </Main>

                <OrbWidget onClick={() => setIsGhostShardOpen(!isGhostShardOpen)} title="GHOST SUPPORT ORB">
                    <div style={{fontSize:'10px', color:'#fff', fontWeight:'bold', transform: 'translateZ(10px)'}}>AI</div>
                </OrbWidget>

                {isGhostShardOpen && (
                    <GhostShardWindow>
                        <Title style={{marginBottom:10, fontSize:'0.75rem'}}>GHOST SUPPORT SHARD</Title>
                        <Log style={{height:250, marginBottom:10}}>
                            {chat.map((c, i) => <div key={i} style={{marginBottom:5}}><span style={{color:c.s==='JARVIS'?'#00AAFF':'#fff', fontWeight:'bold'}}>[{c.s}]:</span> {c.t}</div>)}
                        </Log>
                        <InputField 
                            placeholder="ISSUE MANDATE..." value={input} 
                            onChange={e => setInput(e.target.value)} 
                            onKeyPress={e => e.key === 'Enter' && handleSend()}
                            autoFocus
                        />
                    </GhostShardWindow>
                )}
            </Root>
        </ThemeProvider>
    );
};

export default CreatorDashboard;
