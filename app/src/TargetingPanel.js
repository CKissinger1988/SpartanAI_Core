import React, { useState, useEffect, useRef } from 'react';
import { Card, Input, Button, List, Tag } from 'antd';
import { AimOutlined, PlusOutlined } from '@ant-design/icons';

const TargetingPanel = ({ onTargetSelect }) => {
    const [targets, setTargets] = useState([
        { id: '192.168.1.101', type: 'IP' },
        { id: 'scan-results.local', type: 'DOMAIN' }
    ]);
    const [inputValue, setInputValue] = useState('');

    const handleAddTarget = () => {
        if (!inputValue || targets.some(t => t.id === inputValue)) return;
        // Simple regex to differentiate IP from domain
        const type = /^[0-9.]+$/.test(inputValue) ? 'IP' : 'DOMAIN';
        setTargets([...targets, { id: inputValue, type }]);
        setInputValue('');
    };

    return (
        <Card title="Manual Target Acquisition" size="small" bordered={false}>
            <Input.Group compact>
                <Input
                    style={{ width: 'calc(100% - 100px)' }}
                    placeholder="Enter IP or Domain..."
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onPressEnter={handleAddTarget}
                />
                <Button icon={<PlusOutlined />} onClick={handleAddTarget}>Acquire</Button>
            </Input.Group>
            <List
                size="small"
                dataSource={targets}
                renderItem={item => (
                    <List.Item
                        actions={[<Button size="small" icon={<AimOutlined />} onClick={() => onTargetSelect(item.id)}>Select</Button>]}
                    >
                        <Tag color={item.type === 'IP' ? 'blue' : 'geekblue'}>{item.type}</Tag>
                        {item.id}
                    </List.Item>
                )}
                style={{ marginTop: '10px', height: '150px', overflowY: 'auto' }}
            />
        </Card>
    );
};

export default TargetingPanel;
