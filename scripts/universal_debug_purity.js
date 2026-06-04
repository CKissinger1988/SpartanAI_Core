import { execSync } from 'child_process';

console.log('\x1b[94m\x1b[1m--- Universal Debug Purity Check ---\x1b[0m');
try {
  const output = execSync('node scripts/unbox_protocol.cjs --dry-run', { encoding: 'utf8' });
  const sanitizingLines = output.split('\n').filter(line => line.includes('[*] Sanitizing'));
  
  if (sanitizingLines.length > 0) {
    
    sanitizingLines.forEach(line => ));
    
    
  } else {
    console.log('\x1b[92m[+] Purity check passed! Codebase is clean.\x1b[0m');
    process.exit(0);
  }
} catch (error) {
  
  
}

