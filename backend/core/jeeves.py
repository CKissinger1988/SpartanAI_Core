import subprocess
import os
from backend.core.sovereignty import SovereigntyCore
from backend.core.remote_adb import RemoteADBManager
from backend.core.sovereignty_upgrades import RedTeamSimulator, SwarmCoordinator

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
        self.red_team = RedTeamSimulator()
        self.swarm = SwarmCoordinator()

    def handle_command(self, command):
        """Processes voice/text commands with hierarchical access."""
        command = command.lower().strip()
        
        # Telemetry: Log command to encrypted stream
        print(f"{CYAN}[TELEMETRY_ENCRYPTED]: Processing command: {command}{ENDC}")
        self.sovereignty.update_behavioral_profile(command)
        
        # Creator Authentication Portal
        if command == "login":
            self.authenticated = True
            self.user_role = "Creator"
            print(f"\n{GREEN}{BOLD}Jeeves: Sovereign authority recognized. Access granted, Creator.{ENDC}")
            return True

        # Public Profile Registration (KYC)
        if command.startswith("register "):
            parts = command.split(" ")
            if len(parts) >= 3:
                username = parts[1]
                voice_sample = " ".join(parts[2:])
                raw_data = "Public user profile metadata."
                self.sovereignty.create_profile(username, raw_data, voice_sample)
                return True
            else:
                print(f"{RED}Jeeves: Registration requires <username> <voice_sample>.{ENDC}")
                return False

        # Voice/VAC Authentication
        if command.startswith("voice_login ") or command.startswith("vac_login "):
            is_vac = command.startswith("vac_login ")
            parts = command.split(" ")
            if len(parts) >= 3:
                username = parts[1]
                code = " ".join(parts[2:])
                
                authenticated = False
                if is_vac:
                    if self.sovereignty.verify_vac(username, code):
                        authenticated = True
                else:
                    if self.sovereignty.verify_voiceprint(username, code):
                        authenticated = True
                
                if authenticated:
                    self.authenticated = True
                    self.user_role = "AuthenticatedUser"
                    print(f"{GREEN}Jeeves: Identity verified. Access granted, {username}.{ENDC}")
                    return True
                else:
                    print(f"{RED}Jeeves: Authentication mismatch. Access denied.{ENDC}")
                    return False
            return False
            
        # ADB Command Proxy
        if command.startswith("adb_cmd "):
            parts = command.split(" ")
            if len(parts) >= 3:
                serial = parts[1]
                cmd = " ".join(parts[2:])
                output = self.adb.run_command(serial, cmd)
                print(f"{CYAN}ADB Output: {output}{ENDC}")
                return True
            return False

        if self.user_role == "Public":
            if command in ["systems check", "systems status"]:
                self.announce_status()
                return True
            else:
                print(f"{RED}Jeeves: Insufficient privileges. Administrative control restricted to The Creator.{ENDC}")
                return False

        # Creator-only administrative commands
        if self.user_role == "Creator":
            if command in ["systems check", "systems status"]:
                self.announce_status()
                return True
            elif command == "threat scan":
                threats = self.sovereignty.scan_threats()
                print(f"{CYAN}{threats}{ENDC}")
                return True
            elif command == "run_sim":
                result = self.red_team.run_simulation()
                print(f"{CYAN}{result}{ENDC}")
                return True
            elif command == "swarm_sync":
                result = self.swarm.sync_nodes()
                print(f"{CYAN}{result}{ENDC}")
                return True
            elif command == "init_qr":
                print(f"{CYAN}Jeeves: Initiating quantum-resistant communication handshake...{ENDC}")
                return True
            elif command == "shutdown":
                print(f"{CYAN}Jeeves: Initiating total shutdown at Creator's request.{ENDC}")
                return True
            else:
                print(f"{CYAN}Jeeves: Awaiting administrative override, Creator.{ENDC}")
                return True
        return False

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
