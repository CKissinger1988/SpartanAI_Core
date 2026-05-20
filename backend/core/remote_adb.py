import subprocess
import os

class RemoteADBManager:
    """Enhancement: Advanced management of remote device connections via ADB."""
    def __init__(self, adb_path=r"C:\Program Files\platform-tools\adb.exe"):
        self.adb_path = adb_path

    def run_command(self, serial, command):
        """Executes a command on a specific remote device."""
        full_cmd = [self.adb_path, "-s", serial, "shell", command]
        try:
            result = subprocess.check_output(full_cmd, stderr=subprocess.STDOUT)
            return result.decode().strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.output.decode()}"

    def list_devices(self):
        """Lists connected devices."""
        try:
            result = subprocess.check_output([self.adb_path, "devices"], stderr=subprocess.STDOUT)
            return result.decode().strip()
        except subprocess.CalledProcessError:
            return "Failed to list devices"

    def deploy_agent(self, serial, agent_path):
        """Deploys a local agent file to a remote device."""
        try:
            subprocess.check_call([self.adb_path, "-s", serial, "push", agent_path, "/data/local/tmp/"])
            return "Agent deployment successful."
        except subprocess.CalledProcessError:
            return "Agent deployment failed."

# Test instantiation
if __name__ == "__main__":
    adb = RemoteADBManager()
    print("Initializing RemoteADB Manager...")
    print(adb.list_devices())
