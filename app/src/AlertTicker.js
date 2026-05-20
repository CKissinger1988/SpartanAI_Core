import React, { useState, useEffect } from 'react';
import { Alert } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';

const ipcRenderer = window.electronAPI?.ipcRenderer;

const AlertTicker = () => {
    const [alert, setAlert] = useState(null);

    useEffect(() => {
        if (!ipcRenderer) return;
        const handleAlert = (event, newAlert) => {
            setAlert(newAlert);
            setTimeout(() => setAlert(null), 8000);
        };
        ipcRenderer.on('system.alert', handleAlert);
        return () => ipcRenderer.removeAllListeners('system.alert');
    }, []);

    if (!alert) {
        return (
             <div style={{ position: 'absolute', top: 0, width: '100%', zIndex: 1000, textAlign: 'center', padding: '4px', background: 'rgba(15, 23, 42, 0.8)', color: '#64748b', fontSize: '12px' }}>
                SYSTEM STATUS: NOMINAL. ALL VECTORS SECURE.
            </div>
        );
    }

    return (
        <div style={{ position: 'absolute', top: 0, width: '100%', zIndex: 1000 }}>
            <Alert
                message={<span style={{ fontWeight: 'bold' }}>TACTICAL ALERT: {alert.title}</span>}
                description={alert.message}
                type={alert.type || 'warning'}
                showIcon
                banner
                closable
                onClose={() => setAlert(null)}
            />
        </div>
    );
};

export default AlertTicker;
