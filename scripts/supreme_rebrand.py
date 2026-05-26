import os
import re

def rebrand_path(path):
    # Rebrand file/folder name
    dirname, basename = os.path.split(path)
    new_basename = basename.replace('SentinelAI', 'SpartanAI').replace('Sentinel', 'Spartan').replace('sentinelai', 'spartanai').replace('sentinel', 'spartan')
    new_path = os.path.join(dirname, new_basename)
    if path != new_path:
        os.rename(path, new_path)
        return new_path
    return path

def rebrand_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        new_content = content.replace('SentinelAI', 'SpartanAI').replace('Sentinel', 'Spartan').replace('sentinelai', 'spartanai').replace('sentinel', 'spartan')
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
    except Exception:
        pass

def process_recursive(base_dir):
    for root, dirs, files in os.walk(base_dir, topdown=False):
        for f in files:
            f_path = os.path.join(root, f)
            rebrand_content(f_path)
            rebrand_path(f_path)
        for d in dirs:
            d_path = os.path.join(root, d)
            rebrand_path(d_path)

if __name__ == "__main__":
    targets = [
        'C:\\GitHub\\SentinelAI_Hub_Master',
        'C:\\GitHub\\SentinelAI_Security_Core',
        'C:\\GitHub\\SentinelAI_Server_Final_v50'
    ]
    for target in targets:
        if os.path.exists(target):
            process_recursive(target)
            # Try to rename root
            try:
                new_root = target.replace('SentinelAI', 'SpartanAI')
                os.rename(target, new_root)
                print(f"Successfully rebranded root: {target} -> {new_root}")
            except Exception as e:
                print(f"Failed to rebrand root {target}: {e}")
