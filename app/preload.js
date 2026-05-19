const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    ipcRenderer: {
        invoke: (channel, ...args) => ipcRenderer.invoke(channel, ...args),
        send: (channel, ...args) => ipcRenderer.send(channel, ...args),
        on: (channel, func) => {
            const subscription = (event, ...args) => func(event, ...args);
            ipcRenderer.on(channel, subscription);
        },
        removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel)
    }
});