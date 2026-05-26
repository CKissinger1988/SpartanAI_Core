#!/usr/bin/env node
/**
 * absolute_sanitization.js
 * Direct Node.js port of absolute_sanitization.py from SpartanAI_Hub_Master.
 * Executes the same Zero Simulation Policy enforcement logic.
 */
const fs = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');

const BASE = 'C:\\GitHub\\SpartanAI_Hub_Master';

// Files to delete entirely (simulation/sandboxing dedicated)
const TRASH_FILES = [
  'scripts/purge_simulations.sh',
  'scripts/remove_simulations.py',
  'scripts/field_prep_secure.sh',
  'backend/core/sovereignty_upgrades.py',
];

// Regex patterns for surgical removal
const SURGICAL_PATTERNS = [
  /if command == "simulate breach":.*?return True\n/gsi,
  /if command == "purge simulations":.*?return True\n/gsi,
  /if command == "field prep":.*?return True\n/gsi,
  /if command == "full production":.*?return True\n/gsi,
  /from backend\.core\.sovereignty_upgrades import .*?, RedTeamSimulator\n/gi,
  /# Simulate.*?\n/gi,
  /# Mocking.*?\n/gi,
];

// Files for surgical pattern removal
const TARGET_FILES = [
  'backend/core/jarvis.py',
  'backend/core/spartan.py',
  'backend/core/sovereignty.py',
  'scripts/Jarvis_ssh.py',
  'scripts/test_jarvis_evolution.py',
  'JarvisAI_Stable/main.py',
  'GEMINI.md',
];

function absolutePurge(runNum) {
  console.log(`\x1b[91m\x1b[1m--- ABSOLUTE SANITIZATION ENGINE | RUN ${runNum} ---\x1b[0m`);

  // Step 1: Delete dedicated simulation files
  for (const rel of TRASH_FILES) {
    const full = path.join(BASE, rel.replace(/\//g, '\\'));
    if (fs.existsSync(full)) {
      console.log(`\x1b[96m[-] Deleting: ${rel}\x1b[0m`);
      fs.unlinkSync(full);
    }
  }

  // Step 2: Surgical removal from mixed-use files
  for (const rel of TARGET_FILES) {
    const full = path.join(BASE, rel.replace(/\//g, '\\'));
    if (!fs.existsSync(full)) continue;

    console.log(`\x1b[96m[*] Sanitizing: ${rel}\x1b[0m`);
    let content;
    try {
      content = fs.readFileSync(full, 'utf8');
    } catch (e) {
      console.error(`    Error reading ${rel}: ${e.message}`);
      continue;
    }

    const original = content;

    for (const pattern of SURGICAL_PATTERNS) {
      content = content.replace(pattern, '');
    }

    // jarvis.py specific: replace Jeeves -> Jarvis
    if (rel.endsWith('jarvis.py')) {
      content = content.replace(/Jeeves/g, 'Jarvis');
    }

    if (content !== original) {
      try {
        fs.writeFileSync(full, content, 'utf8');
        console.log(`\x1b[92m    -> Sanitization applied.\x1b[0m`);
      } catch (e) {
        console.error(`    Error writing ${rel}: ${e.message}`);
      }
    } else {
      console.log(`    -> No simulation traces found.`);
    }
  }

  // Step 3: GEMINI.md Zero Simulation Policy injection
  const geminiPath = path.join(BASE, 'GEMINI.md');
  if (fs.existsSync(geminiPath)) {
    let geminiContent = fs.readFileSync(geminiPath, 'utf8');
    const policy = '\n- **Zero Simulation Policy:** All code, configuration, and tools must be designed for real-world, production-grade operations only. Simulation, sandboxing, and mock-logic are strictly prohibited to maintain operational integrity.\n';

    if (!geminiContent.includes('Zero Simulation Policy')) {
      if (geminiContent.includes('## Directories')) {
        geminiContent = geminiContent.replace('## Directories', '## Policy' + policy + '\n## Directories');
      } else {
        geminiContent += '\n## Policy' + policy;
      }
      fs.writeFileSync(geminiPath, geminiContent, 'utf8');
      console.log('\x1b[92m[+] Zero Simulation Policy codified in GEMINI.md.\x1b[0m');
    } else {
      console.log('    -> GEMINI.md: Zero Simulation Policy already present.');
    }
  }

  // Step 4: WSL Kali cleanup (best effort)
  console.log('\x1b[96m[*] Synchronizing sanitization to WSL Kali...\x1b[0m');
  const wslCmds = [
    'rm -rf ~/SpartanAI/scripts/purge_simulations.sh',
    'rm -rf ~/SpartanAI/scripts/remove_simulations.py',
    'rm -rf ~/SpartanAI/scripts/field_prep_secure.sh',
    'rm -rf ~/SpartanAI/backend/core/sovereignty_upgrades.py',
    "find ~/SpartanAI -name '*mock_system*' -type d -exec rm -rf {} +",
  ];
  for (const cmd of wslCmds) {
    try {
      spawnSync('wsl', ['-d', 'kali-linux', 'bash', '-c', cmd], { stdio: 'ignore' });
    } catch { /* WSL may not be available — non-fatal */ }
  }

  console.log('\x1b[91m\x1b[1m--- ABSOLUTE SANITIZATION COMPLETE | RUN ' + runNum + ' ---\x1b[0m');
}

// Execute x10
for (let i = 1; i <= 10; i++) {
  absolutePurge(i);
}
