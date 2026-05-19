// Mock window.electronAPI for Electron BEFORE importing anything that uses it
window.electronAPI = {
    ipcRenderer: {
        on: jest.fn(),
        send: jest.fn(),
        invoke: jest.fn().mockImplementation((channel, args) => {
            if (channel === 'auth.login') return Promise.resolve({ status: 'success', username: 'test', role: 'operator' });
            if (channel === 'system.getStats') return Promise.resolve({ cpu: 10, mem: 20 });
            return Promise.resolve({});
        }),
        removeAllListeners: jest.fn()
    }
};

import React from 'react';
import { render, screen, fireEvent, act, waitFor } from '@testing-library/react';
const SentinelHub = require('./SentinelHub').default;

// Mock components
jest.mock('./TerminalComponent', () => () => <div data-testid="terminal">Terminal</div>);
jest.mock('./ChatComponent', () => () => <div data-testid="chat">Chat</div>);
jest.mock('./ToolDashboard', () => () => <div data-testid="tools">Tools</div>);
jest.mock('./MatrixBackground', () => () => <div data-testid="matrix">Matrix</div>);

describe('SentinelHub', () => {
  test('renders login screen initially', () => {
    render(<SentinelHub />);
    expect(screen.getByText(/RESTRICTED ACCESS TERMINAL/i)).toBeInTheDocument();
  });

  test('switches to dashboard after login', async () => {
    render(<SentinelHub />);
    
    // Mock login
    const userBtn = screen.getByText('INIT_UPLINK');
    const userInput = screen.getByLabelText(/OPERATOR_ID/i);
    const passInput = screen.getByLabelText(/ACCESS_KEY/i);

    fireEvent.change(userInput, { target: { value: 'test' } });
    fireEvent.change(passInput, { target: { value: 'pass' } });
    
    await act(async () => {
        fireEvent.click(userBtn);
    });

    await waitFor(() => {
        expect(screen.getByText(/MAIN_SHELL/i)).toBeInTheDocument();
    });
  });
});
