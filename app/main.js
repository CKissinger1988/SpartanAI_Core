const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const os = require('os');
const { spawn } = require('child_process');
const pty = require('node-pty');
const si = require('systeminformation');

// Jarvis/Gemini Integration
const { PythonShell } = require('python-shell');
const JARVIS_PATH = path.join(__dirname, '..', 'JarvisAI_Stable');

let mainWindow;
const shell = os.platform() === 'win32' ? 'powershell.exe' : 'bash';

function createWindow() {
  const isKiosk = process.argv.includes('--kiosk');

  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    kiosk: isKiosk,
    frame: !isKiosk,
    fullscreen: isKiosk,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  mainWindow.loadFile(path.join(__dirname, 'dist', 'index.html'));

  // Real Terminal Backend
  const ptyProcess = pty.spawn(shell, [], {
    name: 'xterm-color',
    cols: 80,
    rows: 30,
    cwd: process.env.HOME,
    env: process.env
  });

  ptyProcess.on('data', (data) => {
    mainWindow.webContents.send('terminal.incomingData', data);
  });

  ipcMain.on('terminal.keystroke', (event, data) => {
    ptyProcess.write(data);
  });

  // System Information
  ipcMain.handle('system.getStats', async () => {
    const cpu = await si.currentLoad();
    const mem = await si.mem();
    return { cpu: cpu.currentLoad, mem: (mem.active / mem.total) * 100 };
  });

  ipcMain.on('tool.run', (event, tool) => {
    ptyProcess.write(tool + '\r');
  });

  // Unified AI Handler (Jarvis/Gemini)
  ipcMain.handle('ai.command', async (event, command) => {
    return new Promise((resolve) => {
      // Check if command is a technical OS command or an AI request
      const isAI = /^(jarvis|gemini|ask|analyze|explain)/i.test(command);

      if (isAI) {
        const engine = command.toLowerCase().startsWith('gemini') ? 'gemini' : 'auto';
        const prompt = command.replace(/^(jarvis|gemini|ask|analyze|explain)\s*/i, '');

        let options = {
          mode: 'text',
          pythonPath: 'python',
          pythonOptions: ['-u'], // get print results in real-time
          scriptPath: JARVIS_PATH,
          args: [engine, prompt]
        };

        PythonShell.run('main.py', options).then(results => {
          resolve(results.join('\n'));
        }).catch(err => {
          resolve(`AI ERROR: ${err.message}`);
        });
      } else {
        const { exec } = require('child_process');
        exec(command, { cwd: process.env.HOME }, (error, stdout, stderr) => {
          if (error) {
            resolve(`ERROR: ${error.message}`);
            return;
          }
          if (stderr && !stdout) {
            resolve(`STDERR: ${stderr}`);
            return;
          }
          resolve(stdout || 'COMMAND EXECUTED SUCCESSFULLY');
        });
      }
    });
  });

  ipcMain.handle('ai.generate', async (event, { engine, prompt }) => {
    return new Promise((resolve) => {
      let options = {
        mode: 'text',
        pythonPath: 'python',
        scriptPath: JARVIS_PATH,
        args: [engine || 'auto', prompt]
      };

      PythonShell.run('main.py', options).then(results => {
        resolve(results.join('\n'));
      }).catch(err => {
        resolve(`AI ERROR: ${err.message}`);
      });
    });
  });

  // Authentication Handler
  ipcMain.handle('auth.login', async (event, { username, password }) => {
    return new Promise((resolve) => {
      let options = {
        mode: 'text',
        pythonPath: 'python',
        scriptPath: path.join(__dirname, '..', 'backend'),
        args: ['auth', username, password]
      };

      PythonShell.run('user_manager.py', options).then(results => {
        try {
          resolve(JSON.parse(results[results.length - 1]));
        } catch (e) {
          resolve({ status: 'error', message: 'Auth engine failure' });
        }
      }).catch(err => {
        resolve({ status: 'error', message: err.message });
      });
    });
  });

  // Exploit DB Handler
  ipcMain.handle('exploit.manage', async (event, { action, payload }) => {
    return new Promise((resolve) => {
      let args = [];
      if (action === 'scan') args = ['scan', payload];
      else if (action === 'update') args = ['update'];
      else if (action === 'list') args = ['list'];

      let options = {
        mode: 'text',
        pythonPath: 'python',
        scriptPath: path.join(__dirname, '..', 'backend'),
        args: args
      };

      PythonShell.run('exploit_manager.py', options).then(results => {
        try {
          resolve(JSON.parse(results[results.length - 1]));
        } catch (e) {
          resolve({ status: 'error', message: 'Failed to parse response' });
        }
      }).catch(err => {
        resolve({ status: 'error', message: err.message });
      });
    });
  });

  // Trigger backend bootstrap on launch
  const initScripts = [
    'bootstrap.py',
    'ai_init.py'
  ];

  initScripts.forEach(script => {
    const proc = spawn('python', [path.join(__dirname, '..', 'backend', script)]);
    proc.stdout.on('data', (data) => console.log(`${script}: ${data}`));
    proc.stderr.on('data', (data) => console.error(`${script} ERROR: ${data}`));
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
