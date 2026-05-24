import os
import shutil
import subprocess

# Scanning parameters for Universal Ingestion
SCAN_ROOTS = ["C:/Users/ckiss/Games", "C:/Users/ckiss/ES-DE", "C:/Users/ckiss/workspace"]
TARGET_OS_DIR = "workspace/jarvis_os"

# File extensions to prioritize for total ingestion
TARGET_EXTENSIONS = ('.exe', '.iso', '.zip', '.tar.gz', '.bin', '.cue', '.iso', '.nes', '.smc', '.gba', '.n64', '.rom')

def run_universal_ingestion():
    if not os.path.exists(TARGET_OS_DIR):
        os.makedirs(TARGET_OS_DIR)

    for root_dir in SCAN_ROOTS:
        if not os.path.exists(root_dir):
            continue
            
        for root, dirs, files in os.walk(root_dir):
            # Integrate Source Code (look for .git)
            if '.git' in dirs:
                repo_name = os.path.basename(root)
                target_repo = os.path.join(TARGET_OS_DIR, "source_code", repo_name)
                if not os.path.exists(target_repo):
                    shutil.copytree(root, target_repo, dirs_exist_ok=True)
            
            # Integrate Games/ROMs
            for file in files:
                if file.lower().endswith(TARGET_EXTENSIONS):
                    game_path = os.path.join(root, file)
                    rel_path = os.path.relpath(game_path, root_dir)
                    target_path = os.path.join(TARGET_OS_DIR, "games", rel_path)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy2(game_path, target_path)

    return "Universal ingestion complete."
