import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { AnsiUp } from 'ansi_up';

const ansi_up = new AnsiUp();

const Root = styled.div`
    background: #fff;
    border: 1px solid ${props => props.theme.colors.border}44;
    border-radius: 20px;
    height: 300px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.02);
`;

const TerminalHeader = styled.div`
    padding: 12px 20px;
    background: rgba(0, 170, 255, 0.05);
    border-bottom: 1px solid ${props => props.theme.colors.border}44;
    font-size: 0.7rem;
    font-weight: 800;
    color: ${props => props.theme.colors.primary};
    text-transform: uppercase;
    letter-spacing: 2px;
`;

const Console = styled.div`
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    font-family: 'Fira Code', monospace;
    font-size: 0.75rem;
    color: #2C3E50;
    line-height: 1.5;
    background: #fff;
    -webkit-overflow-scrolling: touch;

    &::-webkit-scrollbar { width: 4px; }
    &::-webkit-scrollbar-thumb { background: ${props => props.theme.colors.border}; border-radius: 2px; }
`;

const Line = styled.div`
    margin-bottom: 4px;
    white-space: pre-wrap;
    word-break: break-all;
    border-left: 2px solid transparent;
    padding-left: 10px;
    transition: 0.2s;

    &:hover {
        border-left-color: ${props => props.theme.colors.primary};
        background: rgba(0, 170, 255, 0.02);
    }
`;

const ipcRenderer = window.electronAPI?.ipcRenderer;

const MiniTerminal = ({ title, channel }) => {
    const [output, setOutput] = useState([]);
    const contentRef = useRef(null);

    useEffect(() => {
        if (!ipcRenderer) return;
        const handleData = (event, data) => {
            setOutput(prev => [...prev.slice(-100), ansi_up.ansi_to_html(data)]);
        };
        ipcRenderer.on(channel, handleData);
        ipcRenderer.send('monitor.start', channel);
        return () => ipcRenderer.removeAllListeners(channel);
    }, [channel]);

    useEffect(() => {
        if (contentRef.current) contentRef.current.scrollTop = contentRef.current.scrollHeight;
    }, [output]);

    return (
        <Root>
            <TerminalHeader>{title}</TerminalHeader>
            <Console ref={contentRef}>
                {output.map((line, index) => (
                    <Line key={index} dangerouslySetInnerHTML={{ __html: line }} />
                ))}
            </Console>
        </Root>
    );
};

export default MiniTerminal;
