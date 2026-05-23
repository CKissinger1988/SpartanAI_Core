import React, { useState } from 'react';
import styled, { ThemeProvider } from 'styled-components';
import { 
    Activity, 
    Crosshair, 
    Terminal as TerminalIcon, 
    Bot, 
    User, 
    Settings,
    Menu as MenuIcon,
    ChevronLeft
} from 'lucide-react';
import { theme } from './theme';
import AxiomDashboard from './AxiomDashboard'; 
import AxiomOSD from './AxiomOSD';

const Root = styled.div`
    height: 100vh;
    width: 100vw;
    background-color: ${props => props.theme.colors.bg};
    display: flex;
    overflow: hidden;
    color: ${props => props.theme.colors.text};
    font-family: 'Inter', sans-serif;
`;

const Sidebar = styled.aside`
    width: ${props => props.collapsed ? '80px' : '280px'};
    background: ${props => props.theme.colors.sidebar};
    border-right: 1px solid ${props => props.theme.colors.border};
    display: flex;
    flex-direction: column;
    transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1000;
    box-shadow: 10px 0 30px rgba(0,0,0,0.02);
`;

const SidebarHeader = styled.div`
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: ${props => props.collapsed ? 'center' : 'space-between'};
    padding: 0 25px;
    border-bottom: 1px solid ${props => props.theme.colors.border}44;
`;

const Logo = styled.div`
    font-size: 1.2rem;
    font-weight: 900;
    color: ${props => props.theme.colors.primary};
    letter-spacing: 4px;
    display: ${props => props.collapsed ? 'none' : 'block'};
    text-transform: uppercase;
`;

const CollapseBtn = styled.div`
    cursor: pointer;
    color: ${props => props.theme.colors.textSecondary};
    padding: 8px;
    border-radius: 10px;
    transition: 0.3s;
    &:hover { background: rgba(0, 170, 255, 0.05); color: ${props => props.theme.colors.primary}; }
`;

const NavList = styled.nav`
    flex: 1;
    padding: 20px 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
`;

const NavItem = styled.div`
    padding: 18px 20px;
    border-radius: 15px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 15px;
    color: ${props => props.active ? props.theme.colors.primary : props.theme.colors.textSecondary};
    background: ${props => props.active ? 'rgba(0, 170, 255, 0.08)' : 'transparent'};
    font-weight: 700;
    font-size: 0.9rem;
    transition: 0.3s;
    min-height: 55px;

    &:hover {
        color: ${props => props.theme.colors.primary};
        background: rgba(0, 170, 255, 0.04);
        transform: translateX(5px);
    }

    svg { flex-shrink: 0; }
    span { display: ${props => props.collapsed ? 'none' : 'block'}; }
`;

const Main = styled.div`
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
`;

const Header = styled.header`
    height: 70px;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid ${props => props.theme.colors.border}44;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30px;
`;

const HeaderStatus = styled.div`
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    display: flex;
    gap: 20px;
`;

const Content = styled.main`
    flex: 1;
    overflow-y: auto;
    background: transparent;
    -webkit-overflow-scrolling: touch;
`;

const UserProfile = styled.div`
    padding: 20px;
    border-top: 1px solid ${props => props.theme.colors.border}44;
    display: flex;
    align-items: center;
    justify-content: ${props => props.collapsed ? 'center' : 'flex-start'};
    gap: 15px;
`;

const Avatar = styled.div`
    width: 40px;
    height: 40px;
    background: #fff;
    border: 2px solid ${props => props.theme.colors.primary};
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 10px ${props => props.theme.colors.glow};
`;

const AxiomV2 = ({ user }) => {
    const [collapsed, setCollapsed] = useState(false);
    const [view, setView] = useState('DASHBOARD');

    return (
        <ThemeProvider theme={theme}>
            <Root>
                <Sidebar collapsed={collapsed}>
                    <SidebarHeader collapsed={collapsed}>
                        <Logo collapsed={collapsed}>JARVIS</Logo>
                        <CollapseBtn onClick={() => setCollapsed(!collapsed)}>
                            {collapsed ? <MenuIcon size={20} /> : <ChevronLeft size={20} />}
                        </CollapseBtn>
                    </SidebarHeader>
                    <NavList>
                        <NavItem active={view === 'DASHBOARD'} collapsed={collapsed} onClick={() => setView('DASHBOARD')}>
                            <Activity size={20} />
                            <span>Dashboard</span>
                        </NavItem>
                        <NavItem active={view === 'TARGETS'} collapsed={collapsed} onClick={() => setView('TARGETS')}>
                            <Crosshair size={20} />
                            <span>Targets</span>
                        </NavItem>
                        <NavItem active={view === 'TERMINAL'} collapsed={collapsed} onClick={() => setView('TERMINAL')}>
                            <TerminalIcon size={20} />
                            <span>Terminal</span>
                        </NavItem>
                        <NavItem active={view === 'DIAGNOSTICS'} collapsed={collapsed} onClick={() => setView('DIAGNOSTICS')}>
                            <Bot size={20} />
                            <span>Diagnostics</span>
                        </NavItem>
                    </NavList>
                    <UserProfile collapsed={collapsed}>
                        <Avatar><User size={20} /></Avatar>
                        {!collapsed && (
                            <div style={{ display: 'flex', flexDirection: 'column' }}>
                                <div style={{ fontSize: '0.85rem', fontWeight: 900 }}>{user.username.toUpperCase()}</div>
                                <div style={{ fontSize: '0.6rem', color: '#7F8C8D', fontWeight: 700 }}>SUPREME_OPERATOR</div>
                            </div>
                        )}
                    </UserProfile>
                </Sidebar>
                <Main>
                    <Header>
                        <HeaderStatus>
                            <div>UPLINK: <span style={{ color: '#27AE60' }}>SECURE</span></div>
                            <div style={{ opacity: 0.5 }}>JARVIS OS v8.0 "AXIOM"</div>
                        </HeaderStatus>
                        <Settings size={18} style={{ cursor: 'pointer', opacity: 0.5 }} />
                    </Header>
                    <Content>
                        {view === 'DIAGNOSTICS' ? 
                            <AxiomOSD 
                                status={{ confidence: 99.8 }} 
                                cognitive_state={[{ timestamp: '00:01', thought: 'Deep spectral mapping engaged.' }]} 
                                swarm_logs={{ active_agents: 4 }} 
                            /> 
                            : <AxiomDashboard />
                        }
                    </Content>
                </Main>
            </Root>
        </ThemeProvider>
    );
};

export default AxiomV2;
