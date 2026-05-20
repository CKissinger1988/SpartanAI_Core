import React from 'react';
import { Card, List, Button } from 'antd';
import { RobotOutlined } from '@ant-design/icons';

const JarvisRecommendationsPanel = ({ onExecute }) => {
    // This would come from an IPC call to the AI backend
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
        }
    ];

    return (
        <Card title="Jarvis Recommendations" size="small" bordered={false} icon={<RobotOutlined />}>
            <List
                dataSource={recommendations}
                renderItem={item => (
                    <List.Item actions={[<Button size="small" onClick={() => onExecute(item.command)}>Execute</Button>]}>
                        <List.Item.Meta
                            title={<span style={{ color: '#0ea5e9' }}>{item.title}</span>}
                            description={item.description}
                        />
                    </List.Item>
                )}
                 style={{ height: '200px', overflowY: 'auto' }}
            />
        </Card>
    );
};

export default JarvisRecommendationsPanel;
