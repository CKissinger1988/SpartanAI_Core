import os
import json
import subprocess

class EmulatorIntegrationEngine:
    def __init__(self):
        self.config_dir = "workspace/jarvis_os/emulators"
        self.emulator_map = {
            "nes": "RetroArch",
            "gba": "mGBA",
            "iso": "PCSX2",
            "n64": "Project64"
        }

    def detect_emulators(self, search_paths):
        """Scans for installed emulator binaries."""
        discovered = {}
        for path in search_paths:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.endswith((".exe", ".app")):
                        discovered[file] = os.path.join(path, file)
        return discovered

    def link_game_to_emulator(self, game_file):
        """Maps an ingested game to the appropriate emulator binary."""
        ext = game_file.split('.')[-1].lower()
        return self.emulator_map.get(ext, None)

    def launch_game(self, game_path, emulator_path):
        """Executes the game via the linked emulator."""
        subprocess.Popen([emulator_path, game_path])

    def sync_emulator_configs(self, emulator_name, config_source):
        """Normalizes emulator config files for Jarvis OS."""
        dest = os.path.join(self.config_dir, emulator_name, "config")
        os.makedirs(dest, exist_ok=True)
        # Placeholder for config normalization/copy logic
        pass
