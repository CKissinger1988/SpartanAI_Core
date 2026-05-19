// Mock window.electronAPI for Electron BEFORE importing anything that uses it
window.electronAPI = {
    ipcRenderer: {
        on: jest.fn(),
        send: jest.fn(),
        invoke: jest.fn().mockResolvedValue({ cpu: 10, mem: 20 }),
        removeAllListeners: jest.fn()
    }
};

import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
const SentinelHub = require('./SentinelHub').default;

// Mock components
jest.mock('./TerminalComponent', () => () => <div data-testid="terminal">Terminal</div>);
jest.mock('./ChatComponent', () => () => <div data-testid="chat">Chat</div>);
jest.mock('./ToolDashboard', () => () => <div data-testid="tools">Tools</div>);
jest.mock('./MatrixBackground', () => () => <div data-testid="matrix">Matrix</div>);

describe('SentinelHub', () => {
  test('renders navigation buttons', async () => {
    await act(async () => {
        render(<SentinelHub />);
    });
    expect(screen.getByText(/MAIN_SHELL/i)).toBeInTheDocument();
    expect(screen.getByText(/AI_CORE/i)).toBeInTheDocument();
    expect(screen.getByText(/TOOL_VAULT/i)).toBeInTheDocument();
  });

  test('switches tabs correctly', async () => {
    await act(async () => {
        render(<SentinelHub />);
    });
    
    expect(screen.getByTestId('terminal')).toBeInTheDocument();
    
    await act(async () => {
        fireEvent.click(screen.getByText(/AI_CORE/i));
    });
    expect(screen.getByTestId('chat')).toBeInTheDocument();
    
    await act(async () => {
        fireEvent.click(screen.getByText(/TOOL_VAULT/i));
    });
    expect(screen.getByTestId('tools')).toBeInTheDocument();
  });
});
