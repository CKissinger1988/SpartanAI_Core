const { PythonShell } = require('python-shell');
const path = require('path');
const fs = require('fs');

async function testJarvisIntegration() {
    console.log("--- STARTING FRONTEND-TO-JARVIS INTEGRATION TEST ---");

    const JARVIS_PATH = path.join(__dirname, '..', 'JarvisAI_Stable');
    const mainPyPath = path.join(JARVIS_PATH, 'main.py');

    if (!fs.existsSync(mainPyPath)) {
        console.error("ERROR: Jarvis main.py not found at " + mainPyPath);
        process.exit(1);
    }

    const testCommands = [
        { engine: 'auto', prompt: 'systems status' },
        { engine: 'auto', prompt: 'login' },
        { engine: 'auto', prompt: 'view observations' }
    ];

    for (const cmd of testCommands) {
        console.log(`\nExecuting AI Command: [${cmd.engine}] "${cmd.prompt}"`);
        
        let options = {
            mode: 'text',
            pythonPath: 'python',
            pythonOptions: ['-u'],
            scriptPath: JARVIS_PATH,
            args: [cmd.engine, cmd.prompt]
        };

        try {
            const results = await PythonShell.run('main.py', options);
            console.log("Response Received:");
            console.log(results.join('\n'));
        } catch (err) {
            console.error(`ERROR executing command: ${err.message}`);
        }
    }

    console.log("\n--- INTEGRATION TEST COMPLETE ---");
}

testJarvisIntegration();
