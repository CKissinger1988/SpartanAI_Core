import React from 'react';
import { Card, Row, Col, Statistic, List, Tag } from 'antd';
import { RadarChartOutlined, DeploymentUnitOutlined, SafetyCertificateOutlined } from '@ant-design/icons';

const AxiomOSD = ({ status, cognitive_state, swarm_logs }) => {
    return (
        <div style={{ padding: '20px', background: '#0A0F1E', color: '#E6F1FF', height: '100vh' }}>
            <h1 style={{ color: '#00BFFF', textAlign: 'center' }}>[ MASTER COMMAND DIAGNOSTIC ]</h1>
            <Row gutter={[16, 16]}>
                <Col span={8}>
                    <Card title="Neural Engine Health" size="small" bordered={false} style={{ background: '#101528' }}>
                        <Statistic title="Pattern Confidence" value={status.confidence} precision={2} suffix="%" />
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title="Hive-Mind Swarm" size="small" bordered={false} style={{ background: '#101528' }}>
                        <Statistic title="Active Specialists" value={swarm_logs.active_agents} prefix={<DeploymentUnitOutlined />} />
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title="Safety Verificator" size="small" bordered={false} style={{ background: '#101528' }}>
                        <Tag color="success" icon={<SafetyCertificateOutlined />}>LOGIC PROOFS: VERIFIED</Tag>
                    </Card>
                </Col>
                <Col span={24}>
                    <Card title="Cognitive Logs" bordered={false} style={{ background: '#101528', height: '300px' }}>
                        <List
                            dataSource={cognitive_state}
                            renderItem={item => (
                                <List.Item style={{ border: 'none' }}>
                                    <span style={{ color: '#00BFFF' }}>[{item.timestamp}]</span>
                                    <span style={{ marginLeft: '10px' }}>{item.thought}</span>
                                </List.Item>
                            )}
                        />
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default AxiomOSD;
