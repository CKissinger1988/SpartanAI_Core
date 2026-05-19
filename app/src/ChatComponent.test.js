// Mock window.electronAPI for Electron BEFORE importing anything that uses it
window.electronAPI = {
    ipcRenderer: {
        invoke: jest.fn().mockResolvedValue('Mocked AI response')
    }
};

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
const ChatComponent = require('./ChatComponent').default;

describe('ChatComponent', () => {
    // Mock scrollHeight
    beforeEach(() => {
        Object.defineProperty(HTMLElement.prototype, 'scrollHeight', { configurable: true, value: 100 });
    });

    test('renders initial messages', () => {
        render(<ChatComponent />);
        expect(screen.getByText(/NEXUS CORE ONLINE/)).toBeInTheDocument();
    });

    test('sends a message and displays response', async () => {
        render(<ChatComponent />);
        
        const input = screen.getByPlaceholderText('ENTER COMMAND...');
        const button = screen.getByText('SEND');

        fireEvent.change(input, { target: { value: 'test command' } });
        fireEvent.click(button);

        expect(screen.getByText('test command')).toBeInTheDocument();
        
        await waitFor(() => {
            expect(screen.getByText('Mocked AI response')).toBeInTheDocument();
        });
    });
});
