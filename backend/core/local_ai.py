import requests
import json
import subprocess
import os

class LocalIntelligence:
    """Manages local LLM inference via Ollama for sovereign intelligence operations."""
    def __init__(self):
        self.endpoint = "http://localhost:11434/api/generate"
        self.model = "llama3:8b-instruct-q4_K_M" # Recommended for 16GB RAM

    def generate_response(self, prompt, system_prompt="You are Jarvis, a sovereign AI for the NexusAI ecosystem."):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.endpoint, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get('response', "Intelligence error: Empty response.")
            return f"Intelligence error: Code {response.status_code}"
        except Exception as e:
            return f"Intelligence error: Local server unreachable ({e})"

    def ensure_service_active(self):
        """Checks if Ollama is running and attempts to start it if not."""
        try:
            # Check if port is open
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', 11434)) == 0:
                    return True
            
            print("[NEXUS-AI] Starting local intelligence engine (Ollama)...")
            # In WSL Kali, we'd start the service
            subprocess.Popen(["wsl", "-d", "kali-linux", "bash", "-c", "ollama serve"], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except:
            return False
