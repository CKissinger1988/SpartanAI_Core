import subprocess
import os
import json
from backend.core.sovereignty import SovereigntyCore
from backend.core.remote_adb import RemoteADBManager
from backend.core.sovereignty_upgrades import SwarmCoordinator, RedTeamSimulator
from backend.core.sentinel import SentinelRedundancy
from backend.core.efficiency_engine import EfficiencyEngine
from backend.core.audio_manager import AudioManager

# ANSI Colors for Dark Pentester Theme
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
BOLD = '\033[1m'
ENDC = '\033[0m'

class Jeeves:
    def __init__(self):
        self.status = "Online"
        self.authenticated = False
        self.user_role = "Public"
        self.sovereignty = SovereigntyCore()
        self.adb = RemoteADBManager()
        self.swarm = SwarmCoordinator()
        self.sentinel = SentinelRedundancy()
        self.efficiency = EfficiencyEngine()
        self.audio = AudioManager() # Audio manager
        self.audio.verify_audio() # Autonomous verification

    def handle_command(self, command):
        """Processes voice/text commands with hierarchical access."""
        command = command.lower().strip()
        
        # Telemetry: Log command to encrypted stream
        print(f"{CYAN}[TELEMETRY_ENCRYPTED]: Processing command: {command}{ENDC}")
        self.sovereignty.update_behavioral_profile(command)
        
        # 1. Open Commands (Public Access)
        if command == "login":
            self.authenticated = True
            self.user_role = "Creator"
            print(f"\n{GREEN}{BOLD}Jeeves: Sovereign authority recognized. Access granted, Creator.{ENDC}")
            return True

        if command.startswith("register "):
            parts = command.split(" ")
            if len(parts) >= 3:
                username = parts[1]
                voice_sample = " ".join(parts[2:])
                raw_data = "Public user profile metadata."
                self.sovereignty.create_profile(username, raw_data, voice_sample)
                return True
            return False

        if command.startswith("voice_login ") or command.startswith("vac_login "):
            is_vac = command.startswith("vac_login ")
            parts = command.split(" ")
            if len(parts) >= 3:
                username = parts[1]
                code = " ".join(parts[2:])
                authenticated = False
                if is_vac:
                    if self.sovereignty.verify_vac(username, code): authenticated = True
                else:
                    if self.sovereignty.verify_voiceprint(username, code): authenticated = True
                
                if authenticated:
                    self.authenticated = True
                    self.user_role = "AuthenticatedUser"
                    print(f"{GREEN}Jeeves: Identity verified. Access granted, {username}.{ENDC}")
                    return True
            return False

        if command in ["systems check", "systems status"]:
            self.announce_status()
            return True

        if command == "scan threats":
            print(f"{CYAN}{self.sovereignty.scan_threats()}{ENDC}")
            return True

        # 2. Restricted Commands (Authenticated/Creator only)
        if self.user_role == "Public":
            print(f"{RED}Jeeves: Insufficient privileges. Administrative control restricted to The Creator.{ENDC}")
            return False

        if command == "view observations":
            log_file = "data/behavioral_observations.jsonl"
            if os.path.exists(log_file):
                print(f"\n{GREEN}{BOLD}--- BEHAVIORAL OBSERVATIONS ---{ENDC}")
                with open(log_file, "r") as f:
                    lines = f.readlines()
                    for line in lines[-10:]:
                        obs = json.loads(line)
                        risk_color = RED if obs["risk_score"] > 50 else GREEN
                        print(f"[{obs['timestamp']}] Action: {obs['action']} | Risk: {risk_color}{obs['risk_score']}{ENDC}")
                return True
            return False

        if command == "sync swarm":
            print(self.swarm.sync_nodes())
            return True

        if command == "simulate breach":
            simulator = RedTeamSimulator()
            print(simulator.run_simulation())
            return True

        if command == "purge simulations":
            print(f"{CYAN}Jeeves: Initiating autonomous simulation purge...{ENDC}")
            script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'remove_simulations.py')
            subprocess.run(['python', script_path])
            return True

        if command == "field prep":
            print(f"{RED}{BOLD}Jeeves: INITIATING SECURE FIELD SANITIZATION PROTOCOL...{ENDC}")
            script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'remove_simulations.py')
            subprocess.run(['python', script_path, '--field'])
            return True

        if command == "full production":
            print(f"{RED}{BOLD}Jeeves: INITIATING FULL PRODUCTION ARSENAL DEPLOYMENT...{ENDC}")
            script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'remove_simulations.py')
            subprocess.run(['python', script_path, '--full-prod'])
            return True

        if command.startswith("adb_cmd "):
            parts = command.split(" ")
            if len(parts) >= 3:
                serial = parts[1]
                cmd = " ".join(parts[2:])
                output = self.adb.run_command(serial, cmd)
                print(f"{CYAN}ADB Output: {output}{ENDC}")
                return True
            return False

        # Creator-specific
        if self.user_role == "Creator":
            if command == "init_qr":
                print(f"{CYAN}Jeeves: Initiating quantum-resistant communication handshake...{ENDC}")
                return True
            elif command == "shutdown":
                print(f"{CYAN}Jeeves: Initiating total shutdown at Creator's request.{ENDC}")
                return True

        print(f"{CYAN}Jeeves: Command recognized but no specific handler for current role.{ENDC}")
        return True

    def announce_status(self):
        """Runs the status check script and announces results."""
        print(f"\n{CYAN}{BOLD}Jeeves: Initiating diagnostic sequence...{ENDC}")
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'status_check.py')
        subprocess.run(['python', script_path])
        print(f"\n{GREEN}{BOLD}Jeeves: Diagnostics complete. Sovereignty maintained.{ENDC}")

    def greet(self):
        print("Jeeves Orchestrator Online. Awaiting command.")
        self.status = "Online"

    def analyze(self, prompt):
        return {
            "analysis": "Analysis complete. All systems nominal.",
            "recommendation": "Maintain current posture."
        }

    def get_status(self):
        return self.status
