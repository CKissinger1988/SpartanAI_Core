import os

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Replace occurrences
        new_content = content.replace('SENTINELAI', 'SPARTANAI')\
                             .replace('SENTINEL', 'SPARTAN')\
                             .replace('SentinelAI', 'SpartanAI')\
                             .replace('Sentinel', 'Spartan')\
                             .replace('sentinelai', 'spartanai')\
                             .replace('sentinel', 'spartan')
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
    except Exception as e:
        pass

def rename_item(base_path):
    for root, dirs, files in os.walk(base_path, topdown=False):
        # Exclude node_modules and .git
        if 'node_modules' in root or '.git' in root:
            continue
            
        for f in files:
            old_fpath = os.path.join(root, f)
            replace_in_file(old_fpath)
            
            new_f = f.replace('SENTINELAI', 'SPARTANAI').replace('SENTINEL', 'SPARTAN').replace('SentinelAI', 'SpartanAI').replace('Sentinel', 'Spartan').replace('sentinelai', 'spartanai').replace('sentinel', 'spartan')
            if new_f != f:
                new_fpath = os.path.join(root, new_f)
                os.rename(old_fpath, new_fpath)
                
        for d in dirs:
            if 'node_modules' in d or '.git' in d:
                continue
            old_dpath = os.path.join(root, d)
            new_d = d.replace('SENTINELAI', 'SPARTANAI').replace('SENTINEL', 'SPARTAN').replace('SentinelAI', 'SpartanAI').replace('Sentinel', 'Spartan').replace('sentinelai', 'spartanai').replace('sentinel', 'spartan')
            if new_d != d:
                new_dpath = os.path.join(root, new_d)
                os.rename(old_dpath, new_dpath)

if __name__ == '__main__':
    targets = [
        '/mnt/c/GitHub/SpartanAI_Hub_Master',
        '/mnt/c/GitHub/SpartanAI_Security_Core',
        '/mnt/c/GitHub/SpartanAI_Security_Suite',
        '/mnt/c/GitHub/SpartanAI_Server_Final_v50'
    ]
    for target in targets:
        if os.path.exists(target):
            print(f"Rebranding {target}")
            rename_item(target)
