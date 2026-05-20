import React, { useState } from 'react';
import { Row, Col } from 'antd';
import SystemStatusPanel from './SystemStatusPanel';
import TargetingPanel from './TargetingPanel';
import ActionPanel from './ActionPanel';
import JarvisRecommendationsPanel from './JarvisRecommendationsPanel';
import MiniTerminal from './MiniTerminal';
import AlertTicker from './AlertTicker';

const AxiomDashboard = () => {
    const [selectedTarget, setSelectedTarget] = useState(null);
    const ipcRenderer = window.electronAPI?.ipcRenderer;
    
    const handleExecute = (command) => {
        if (!ipcRenderer) return;
        ipcRenderer.send('terminal.keystroke', command + '\r');
    };

    return (
        <div style={{ position: 'relative' }}>
            <AlertTicker />
            <div style={{ paddingTop: '50px' }}>
                <Row gutter={[16, 16]}>
                    <Col span={24}>
                        <SystemStatusPanel />
                    </Col>

                    <Col xs={24} lg={8}>
                        <TargetingPanel onTargetSelect={setSelectedTarget} />
                    </Col>
                    <Col xs={24} lg={8}>
                        <ActionPanel selectedTarget={selectedTarget} onExecute={handleExecute} />
                    </Col>
                    <Col xs={24} lg={8}>
                        <JarvisRecommendationsPanel onExecute={handleExecute} />
                    </Col>

                    <Col xs={24} lg={12}>
                        <MiniTerminal title="IDS Log (Suricata)" channel="monitor.ids" />
                    </Col>
                    <Col xs={24} lg={12}>
                        <MiniTerminal title="Jarvis Operations Log" channel="monitor.jarvis_log" />
                    </Col>
                </Row>
            </div>
        </div>
    );
};

export default AxiomDashboard;
