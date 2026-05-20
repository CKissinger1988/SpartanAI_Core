import React, { useState, useEffect } from 'react';
import { Card, Col, Row, Statistic, Tag } from 'antd';
import { CheckCircleOutlined, SyncOutlined, CloseCircleOutlined } from '@ant-design/icons';

const ipcRenderer = window.electronAPI?.ipcRenderer;

const SystemStatusPanel = () => {
    const [status, setStatus] = useState({
        uplink: { status: 'CONNECTING' },
        database: { status: 'CONNECTING' },
        scanner: { status: 'UNKNOWN' },
        exploitEngine: { status: 'UNKNOWN' },
        overall: 'INITIALIZING'
    });

    useEffect(() => {
        if (!ipcRenderer) return;
        const getStatus = async () => {
            const newStatus = await ipcRenderer.invoke('system.getDetailedStatus');
            setStatus(newStatus);
        };
        const interval = setInterval(getStatus, 2500);
        getStatus();
        return () => clearInterval(interval);
    }, []);

    const getStatusIndicator = (stat) => {
        switch (stat) {
            case 'SECURE': case 'SYNCED': case 'IDLE': case 'CONNECTED': case 'NOMINAL':
                return <Tag icon={<CheckCircleOutlined />} color="success">{stat}</Tag>;
            case 'CONNECTING': case 'SYNCING': case 'SCANNING':
                 return <Tag icon={<SyncOutlined spin />} color="processing">{stat}</Tag>;
            default:
                return <Tag icon={<CloseCircleOutlined />} color="error">{stat}</Tag>;
        }
    };

    return (
        <Card title="System Readiness & Status" size="small" bordered={false}>
            <Row gutter={16}>
                <Col span={5}><Statistic title="Overall Status" valueRender={() => getStatusIndicator(status.overall)} /></Col>
                <Col span={5}><Statistic title="Uplink (TOR)" valueRender={() => getStatusIndicator(status.uplink.status)} /></Col>
                <Col span={5}><Statistic title="Exploit DB" valueRender={() => getStatusIndicator(status.database.status)} /></Col>
                <Col span={5}><Statistic title="Scanner (NMAP)" valueRender={() => getStatusIndicator(status.scanner.status)} /></Col>
                <Col span={4}><Statistic title="Exploit Engine" valueRender={() => getStatusIndicator(status.exploitEngine.status)} /></Col>
            </Row>
        </Card>
    );
};

export default SystemStatusPanel;
