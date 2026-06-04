import os
import re

# Mapping for rebranding (SpartanAI -> SpartanAI)
replacements = {
    r'SpartanAI': 'SpartanAI',
    r'Spartan': 'Spartan',
    r'spartanai': 'spartanai',
    r'spartan': 'spartan',
    r'Jarvis': 'Jarvis', # Ensure Jarvis remains Jarvis
    r'jarvis': 'jarvis'
}

def rebrand_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for pattern, replacement in replacements.items():
            new_content = re.sub(pattern, replacement, new_content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return False

def walk_and_rebrand(root_dir):
    modified_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden and system directories
        if '.git' in dirs: dirs.remove('.git')
        if 'node_modules' in dirs: dirs.remove('node_modules')
        
        for file in files:
            if file.endswith(('.py', '.ps1', '.sh', '.md', '.json', '.js', '.ts', '.html')):
                full_path = os.path.join(root, file)
                if rebrand_file(full_path):
                    modified_files.append(full_path)
    return modified_files

if __name__ == "__main__":
    print("[REBRAND]: Initiating Full Send Rebranding Sweep...")
    modified = walk_and_rebrand('.')
    print(f"[REBRAND]: Modified {len(modified)} files.")
    for f in modified:
        print(f"  [MODIFIED]: {f}")
