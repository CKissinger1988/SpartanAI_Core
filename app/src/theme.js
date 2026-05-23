export const theme = {
    colors: {
        bg: '#F0F4F8', // High-tech light gray/white (I, Robot / VIKI aesthetic)
        sidebar: '#FFFFFF',
        content: '#FFFFFF',
        border: '#D1D9E6',
        text: '#2C3E50',
        textSecondary: '#7F8C8D',
        primary: '#00AAFF', // Signature Sonny Blue
        accent: '#E74C3C', // Alert Red
        success: '#27AE60',
        warning: '#F39C12',
        error: '#C0392B',
        glass: 'rgba(255, 255, 255, 0.7)',
        glow: 'rgba(0, 170, 255, 0.3)',
    },
    effects: {
        neon: (color) => `0 0 10px ${color}, 0 0 20px ${color}44`,
        shadow: '0 8px 32px rgba(31, 38, 135, 0.15)',
        glass: 'backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.18);',
    },
    animations: {
        pulse: 'cubic-bezier(0.4, 0, 0.6, 1) infinite',
    }
};
