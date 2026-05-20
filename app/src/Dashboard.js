import React, { useState, useEffect } from 'react';
import { Card, Col, Row, Statistic, Button, List } from 'antd';
import { ApiOutlined, BugOutlined, ScanOutlined, AimOutlined } from '@ant-design/icons';
import MiniTerminal from './MiniTerminal';

const ipcRenderer = window.electronAPI?.ipcRenderer;

const Dashboard = () => {
    const [exploits, setExploits] = useState([]);

    useEffect(() => {
        const fetchExploits = async () => {
            if (!ipcRenderer) return;
            try {
                const result = await ipcRenderer.invoke('exploit.manage', { action: 'list', payload: 5 });
                if (result && result.length) {
                    setExploits(result);
                }
            } catch (error) {
                console.error("Failed to fetch exploits:", error);
            }
        };
        fetchExploits();
    }, []);

    const handleScan = (command) => {
        if (!ipcRenderer) return;
        ipcRenderer.send('terminal.keystroke', command + '');
        // Optionally switch to terminal tab
    };

    return (
        <div style={{ padding: '1px' }}>
            <Row gutter={[16, 16]}>
                {/* Scan Controls */}
                <Col span={24}>
                    <Card title="Tactical Operations" bordered={false} style={{ background: '#1e293b' }}>
                        <Row gutter={16}>
                            <Col span={6}>
                                <Button type="primary" block icon={<ScanOutlined />} onClick={() => handleScan('nmap -T4 -A -v 192.168.1.0/24')}>
                                    Aggressive LAN Scan
                                </Button>
                            </Col>
                            <Col span={6}>
                                <Button block icon={<AimOutlined />} onClick={() => handleScan('python backend/iot_manager.py scan')}>
                                    Discover IoT Vectors
                                </Button>
                            </Col>
                            <Col span={6}>
                                <Button block icon={<BugOutlined />} onClick={() => handleScan('python backend/exploit_manager.py update')}>
                                    Sync Exploit DB
                                </Button>
                            </Col>
                            <Col span={6}>
                                <Button danger block icon={<ApiOutlined />} onClick={() => handleScan('sudo service tor restart')}>
                                    Rotate TOR Uplink
                                </Button>
                            </Col>
                        </Row>
                    </Card>
                </Col>

                {/* Mini Terminals */}
                <Col xs={24} sm={24} md={12} lg={8}>
                   <MiniTerminal title="Uplink Health (Ping)" channel="monitor.ping" />
                </Col>
                <Col xs={24} sm={24} md={12} lg={8}>
                    <MiniTerminal title="C2 Registry Log" channel="monitor.c2" />
                </Col>
                <Col xs={24} sm={24} md={24} lg={8}>
                     <Card title="Recent Exploits" bordered={false} style={{ background: '#1e293b', height: '300px' }} bodyStyle={{ padding: '0 16px' }}>
                        <List
                            itemLayout="horizontal"
                            dataSource={exploits}
                            renderItem={item => (
                                <List.Item style={{ borderBottom: '1px solid #334155' }}>
                                    <List.Item.Meta
                                        title={<span style={{ color: '#0ea5e9' }}>{item.name}</span>}
                                        description={<span style={{ color: '#94a3b8' }}>{item.cve} - {item.type}</span>}
                                    />
                                </List.Item>
                            )}
                        />
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default Dashboard;
