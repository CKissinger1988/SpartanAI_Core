import React, { useState } from 'react';
import { Layout, Menu } from 'antd';
import styled, { ThemeProvider } from 'styled-components';
import {
    DashboardOutlined,
    AimOutlined,
    CodeOutlined,
    RobotOutlined,
    UserOutlined,
    SettingOutlined
} from '@ant-design/icons';
import { theme } from './theme';
import AxiomDashboard from './AxiomDashboard'; 
import AxiomOSD from './AxiomOSD';

const { Header, Sider, Content } = Layout;

const StyledLayout = styled(Layout)`
    height: 100vh;
    background-color: ${props => props.theme.colors.bg};
`;

const StyledHeader = styled(Header)`
    background: ${props => props.theme.colors.sidebar};
    border-bottom: 1px solid ${props => props.theme.colors.border};
    color: ${props => props.theme.colors.text};
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 24px;
`;

const StyledSider = styled(Sider)`
    background: ${props => props.theme.colors.sidebar};
    border-right: 1px solid ${props => props.theme.colors.border};
    .ant-layout-sider-children {
        display: flex;
        flex-direction: column;
    }
`;

const Logo = styled.div`
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: bold;
    color: ${props => props.theme.colors.primary};
    text-shadow: ${props => props.theme.effects.neon(props.theme.colors.primary)};
`;

const StyledContent = styled(Content)`
    padding: 24px;
    overflow: auto;
    background-color: ${props => props.theme.colors.bg};
`;

const AxiomV2 = ({ user }) => {
    const [collapsed, setCollapsed] = useState(false);
    const [showOSD, setShowOSD] = useState(false);

    return (
        <ThemeProvider theme={theme}>
            <StyledLayout>
                <StyledSider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
                    <Logo>{collapsed ? 'N' : 'NEXUS'}</Logo>
                    <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']} style={{ background: 'transparent', border: 'none', flex: 1 }}>
                        <Menu.Item key="1" icon={<DashboardOutlined />} onClick={() => setShowOSD(false)}>Dashboard</Menu.Item>
                        <Menu.Item key="2" icon={<AimOutlined />}>Targets</Menu.Item>
                        <Menu.Item key="3" icon={<CodeOutlined />}>Terminal</Menu.Item>
                        <Menu.Item key="4" icon={<RobotOutlined />} onClick={() => setShowOSD(true)}>Master Diagnostics</Menu.Item>
                    </Menu>
                     <div style={{ padding: '16px', color: theme.colors.textSecondary, textAlign: 'center' }}>
                        <UserOutlined />
                        {!collapsed && <span style={{ marginLeft: '8px' }}>{user.username}</span>}
                    </div>
                </StyledSider>
                <Layout>
                    <StyledHeader>
                        <div>UPLINK STATUS: <span style={{color: theme.colors.success}}>SECURE</span></div>
                        <div>NEXUS OS v4.0.0 "AXIOM"</div>
                    </StyledHeader>
                    <StyledContent>
                        {showOSD ? 
                            <AxiomOSD status={{confidence: 99.8}} cognitive_state={[{timestamp: '00:01', thought: 'Analyzing security posture...'}]} swarm_logs={{active_agents: 4}} /> 
                            : <AxiomDashboard />
                        }
                    </StyledContent>
                </Layout>
            </StyledLayout>
        </ThemeProvider>
    );
};

export default AxiomV2;
