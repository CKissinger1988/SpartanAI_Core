export const theme = {
    colors: {
        bg: '#0A0F1E', // Very dark blue, almost black
        sidebar: '#101528',
        content: '#191F35',
        border: '#2A314C',
        text: '#E6F1FF',
        textSecondary: '#A2B5D4',
        primary: '#00BFFF', // Deep Sky Blue
        accent: '#FFBF00', // Amber
        success: '#4CAF50',
        warning: '#FFC107',
        error: '#F44336',
    },
    effects: {
        neon: (color) => `0 0 3px ${color}, 0 0 8px ${color}`,
        shadow: '0 4px 12px rgba(0, 0, 0, 0.4)',
    }
};
