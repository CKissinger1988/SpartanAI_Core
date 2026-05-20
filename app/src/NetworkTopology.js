import React, { useState, useEffect } from 'react';
import { Share2, Server, Smartphone, Globe, ShieldCheck, Zap } from 'lucide-react';

const NetworkTopology = () => {
    const [nodes, setNodes] = useState([
        { id: 'master', label: 'MASTER_UPLINK', type: 'core', pos: { x: 400, y: 300 }, status: 'active' },
        { id: 'c2', label: 'C2_REGISTRY', type: 'service', pos: { x: 400, y: 150 }, status: 'active' },
        { id: 'iot-1', label: 'NODE_ALPHA', type: 'iot', pos: { x: 200, y: 200 }, status: 'active' },
        { id: 'iot-2', label: 'NODE_BETA', type: 'iot', pos: { x: 600, y: 200 }, status: 'warning' },
        { id: 'mobile', label: 'MOBILE_HUB', type: 'endpoint', pos: { x: 400, y: 450 }, status: 'active' },
    ]);

    const connections = [
        { from: 'master', to: 'c2' },
        { from: 'master', to: 'iot-1' },
        { from: 'master', to: 'iot-2' },
        { from: 'master', to: 'mobile' },
        { from: 'c2', to: 'mobile' },
    ];

    const COLORS = {
        core: '#0ea5e9',
        service: '#6366f1',
        iot: '#10b981',
        endpoint: '#f59e0b',
        warning: '#ef4444',
        border: '#334155'
    };

    return (
        <div style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h2 style={{ fontSize: '20px', fontWeight: 600, margin: 0 }}>Network Topology</h2>
                    <p style={{ fontSize: '13px', color: '#64748b', margin: '4px 0 0 0' }}>Real-time infrastructure mapping and route visualization.</p>
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                    <button style={{ background: '#1e293b', border: '1px solid #334155', color: '#f8fafc', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Zap size={16} /> Rescan Network
                    </button>
                </div>
            </div>

            <div style={{ flex: 1, background: '#020617', borderRadius: '8px', border: '1px solid #334155', position: 'relative', overflow: 'hidden' }}>
                {/* SVG for connections */}
                <svg style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none' }}>
                    <defs>
                        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
                            <polygon points="0 0, 10 3.5, 0 7" fill="#334155" />
                        </marker>
                    </defs>
                    {connections.map((conn, i) => {
                        const fromNode = nodes.find(n => n.id === conn.from);
                        const toNode = nodes.find(n => n.id === conn.to);
                        return (
                            <line 
                                key={i}
                                x1={fromNode.pos.x} y1={fromNode.pos.y}
                                x2={toNode.pos.x} y2={toNode.pos.y}
                                stroke="#1e293b"
                                strokeWidth="2"
                                strokeDasharray="5,5"
                            />
                        );
                    })}
                </svg>

                {/* Nodes */}
                {nodes.map(node => (
                    <div 
                        key={node.id}
                        style={{
                            position: 'absolute',
                            left: node.pos.x - 40,
                            top: node.pos.y - 40,
                            width: '80px',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            gap: '8px',
                            cursor: 'move'
                        }}
                    >
                        <div style={{ 
                            width: '48px', 
                            height: '48px', 
                            background: '#1e293b', 
                            border: `2px solid ${node.status === 'warning' ? COLORS.warning : COLORS[node.type]}`,
                            borderRadius: '12px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            boxShadow: `0 0 15px ${node.status === 'warning' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(0,0,0,0.5)'}`
                        }}>
                            {node.type === 'core' && <ShieldCheck color={COLORS.core} />}
                            {node.type === 'service' && <Server color={COLORS.service} />}
                            {node.type === 'iot' && <Share2 color={COLORS.iot} />}
                            {node.type === 'endpoint' && <Smartphone color={COLORS.endpoint} />}
                        </div>
                        <div style={{ fontSize: '10px', fontWeight: 600, color: '#94a3b8', textAlign: 'center' }}>{node.label}</div>
                    </div>
                ))}

                {/* Legend */}
                <div style={{ position: 'absolute', bottom: '20px', right: '20px', background: 'rgba(30, 41, 59, 0.8)', padding: '12px', borderRadius: '6px', border: '1px solid #334155', fontSize: '11px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: COLORS.core }} /> CORE_IDENTITY
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: COLORS.service }} /> BACKEND_SERVICE
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: COLORS.iot }} /> IOT_VECTOR
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: COLORS.warning }} /> ALERT_STATE
                    </div>
                </div>
            </div>
        </div>
    );
};

export default NetworkTopology;
