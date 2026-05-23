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
      preload: path.join(__dirname, 'preload.js'),
      additionalArguments: [process.env.NEXUS_PREVIEW === 'true' || !app.isPackaged ? '--preview' : '']
    }
  });

  mainWindow.loadFile(path.join(__dirname, 'dist', 'index.html'));

  // Create Widget
  const isWidgetOnly = process.argv.includes('--widget-only');
  const widgetWindow = new BrowserWindow({
    width: 300,
    height: 200,
    frame: false,
    alwaysOnTop: true,
    show: isWidgetOnly,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });
  widgetWindow.loadFile(path.join(__dirname, 'widget.html'));
  widgetWindow.setPosition(100, 100);

  if (!isWidgetOnly) {
    // Hide widget if not explicitly asked for it or handle as needed
    // widgetWindow.hide();
  }

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

  ipcMain.handle('system.getDetailedStatus', async () => {
    return { status: 'online', uptime: process.uptime(), version: '1.0.0' };
  });

  ipcMain.handle('sys.vitals', async () => {
    const cpu = await si.currentLoad();
    const mem = await si.mem();
    const uptime = os.uptime();
    return {
      status: 'success',
      data: {
        cpu: `${Math.round(cpu.currentLoad)}%`,
        ram: `${Math.round((mem.active / mem.total) * 100)}%`,
        uptime: `${Math.floor(uptime / 3600)}h ${Math.floor((uptime % 3600) / 60)}m`,
        vault: 'SECURE',
        bridge: 'ONLINE',
        nodes: 'SYNCED',
        threat: 'ALPHA',
        learning_rate: '84.2',
        budget_usage: '12%'
      }
    };
  });

  ipcMain.handle('miner.stats', async () => {
    return new Promise((resolve) => {
      let options = {
        mode: 'text',
        pythonPath: 'python',
        scriptPath: path.join(__dirname, '..', 'backend', 'core'),
        args: ['stats']
      };
      PythonShell.run('monetization.py', options).then(results => {
        try {
          resolve({ status: 'success', data: JSON.parse(results[results.length - 1]) });
        } catch (e) {
          resolve({ status: 'error', message: 'Failed to parse miner stats' });
        }
      }).catch(err => resolve({ status: 'error', message: err.message }));
    });
  });

  ipcMain.handle('sys.optimize', async () => {
    return new Promise((resolve) => {
      let options = {
        mode: 'text',
        pythonPath: 'python',
        scriptPath: path.join(__dirname, '..', 'backend', 'core'),
        args: ['optimize']
      };
      PythonShell.run('sentinel.py', options).then(results => {
        resolve({ status: 'success', data: results.join('\n') });
      }).catch(err => resolve({ status: 'error', message: err.message }));
    });
  });

  ipcMain.handle('hexstrike.recon', async (event, { target }) => {
    return new Promise((resolve) => {
      let options = {
        mode: 'text',
        pythonPath: 'python',
        scriptPath: path.join(__dirname, '..', 'backend', 'core'),
        args: ['recon', target]
      };
      PythonShell.run('hexstrike_client.py', options).then(results => {
        resolve({ status: 'success', data: results.join('\n') });
      }).catch(err => resolve({ status: 'error', message: err.message }));
    });
  });

  ipcMain.on('miner.control', (event, action) => {
    let options = {
      mode: 'text',
      pythonPath: 'python',
      scriptPath: path.join(__dirname, '..', 'backend', 'core'),
      args: [action]
    };
    PythonShell.run('monetization.py', options).catch(err => console.error('Miner Control Error:', err));
  });

  ipcMain.on('tool.run', (event, tool) => {
    ptyProcess.write(tool + '\r');
  });

  // Antigravity CLI Handler
  ipcMain.handle('agy.command', async (event, { prompt }) => {
    return new Promise((resolve) => {
      const agyPath = path.join(os.homedir(), 'AppData', 'Local', 'agy', 'bin', 'agy.exe');
      let options = {
        mode: 'text',
        pythonPath: 'python', // Not used but required by some older shells
        args: ['--print', prompt]
      };
      
      const { exec } = require('child_process');
      exec(`"${agyPath}" --print "${prompt}"`, { maxBuffer: 1024 * 1024 * 10 }, (error, stdout, stderr) => {
        if (error) {
          resolve({ status: 'error', message: error.message });
          return;
        }
        resolve({ status: 'success', data: stdout || stderr });
      });
    });
  });

  // Unified AI Handler (Jarvis/Gemini)
  ipcMain.handle('ai.command', async (event, command) => {
    return new Promise((resolve) => {
      // Internal Command Handling
      if (command === 'internal.c2_list') {
        let options = {
          mode: 'text',
          pythonPath: 'python',
          scriptPath: path.join(__dirname, '..', 'backend'),
          args: ['list']
        };
        PythonShell.run('c2_registry.py', options).then(results => {
          resolve(results[results.length - 1]);
        }).catch(err => resolve(JSON.stringify({ status: "error", message: err.message })));
        return;
      }

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

  // IoT & Smart Home Handler
  ipcMain.handle('iot.manage', async (event, { action, params }) => {
    return new Promise((resolve) => {
      let args = [action];
      if (action === 'control') {
        args.push(params.ip, params.port, params.path, params.method);
      }

      let options = {
        mode: 'text',
        pythonPath: 'python',
        scriptPath: path.join(__dirname, '..', 'backend'),
        args: args
      };

      PythonShell.run('iot_manager.py', options).then(results => {
        try {
          resolve(JSON.parse(results[results.length - 1]));
        } catch (e) {
          resolve({ status: 'error', message: 'IoT engine failure' });
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
