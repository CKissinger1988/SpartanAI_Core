// Mock window.electronAPI
const mockInvoke = jest.fn();
const mockSend = jest.fn();

window.electronAPI = {
    ipcRenderer: {
        invoke: mockInvoke,
        send: mockSend
    }
};

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
const ToolDashboard = require('./ToolDashboard').default;

// Mock alert
window.alert = jest.fn();

describe('ToolDashboard', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('renders tools', () => {
        render(<ToolDashboard />);
        expect(screen.getByText('AI Analyze')).toBeInTheDocument();
        expect(screen.getByText('Nmap')).toBeInTheDocument();
    });

    test('runs standard tool', () => {
        render(<ToolDashboard />);
        const nmapBtn = screen.getByText('Nmap');
        fireEvent.click(nmapBtn);
        expect(mockSend).toHaveBeenCalledWith('tool.run', 'nmap -v localhost');
    });

    test('runs analyze tool', async () => {
        mockInvoke.mockResolvedValueOnce('AI result');
        render(<ToolDashboard />);
        const analyzeBtn = screen.getByText('AI Analyze');
        fireEvent.click(analyzeBtn);
        
        await waitFor(() => {
            expect(mockInvoke).toHaveBeenCalledWith('ai.command', 'analyze status');
            expect(window.alert).toHaveBeenCalledWith('AI Analysis:\nAI result');
        });
    });

    test('runs exploit tool when found', async () => {
        mockInvoke.mockResolvedValueOnce({ content: 'payload data', name: 'Exploit 1', url: 'http://test', cve: 'CVE-1234' });
        render(<ToolDashboard />);
        const exploitBtn = screen.getByText('Auto Exploit');
        fireEvent.click(exploitBtn);

        await waitFor(() => {
            expect(mockInvoke).toHaveBeenCalledWith('exploit.manage', { action: 'find', payload: 'CVE-2021-44228' });
            expect(mockSend).toHaveBeenCalledWith('terminal.keystroke', '# AUTO-EXPLOIT ENGAGED: Exploit 1\r');
            expect(mockSend).toHaveBeenCalledWith('terminal.keystroke', '# SOURCE: http://test\r');
            expect(mockSend).toHaveBeenCalledWith('tool.run', 'exploit-launch --cve CVE-1234 --payload-data "cGF5bG9hZCBkYXRh"');
        });
    });
});
