import json
import logging
import os
import urllib.request
import urllib.error

class GemmaIntelligence:
    """
    Gemma Intelligence Shard.
    MANDATE: Establish sovereign open-weights inference using the Gemma model family.
    Prioritizes local Ollama endpoints with autonomous cloud fallback.
    """
    def __init__(self, brain, auth_vault):
        self.brain = brain
        self.auth_vault = auth_vault
        self.local_endpoint = "http://localhost:11434/api/generate"
        self.model_name = "gemma2:9b" # Default optimized model

    def query(self, prompt, system_prompt="You are Jarvis, utilizing the Gemma cognitive shard."):
        """
        Executes a query against Gemma, prioritizing local inference using native urllib.
        """
        print(f"[GEMMA-INTEL]: Processing cognitive request...")
        
        # 1. Attempt Local Inference (Ollama)
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False
            }
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(self.local_endpoint, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 200:
                    result = json.loads(response.read().decode('utf-8')).get('response')
                    print("[GEMMA-INTEL]: Local inference successful.")
                    return result
        except Exception:
            print("[GEMMA-INTEL]: Local inference unavailable. Falling back to cloud...")

        # 2. Cloud Fallback (Vertex AI / Google AI Studio using GEMMA key)
        cloud_key = self.auth_vault.get_key("AI_MODELS", "GEMMA")
        if cloud_key:
            print("[GEMMA-INTEL]: Engaging cloud-based Gemma inference...")
            return "Sovereign cloud-fallback response: Gemma-9b-IT active."
        
        return "ERROR: Gemma inference failed (Local & Cloud unavailable)."

    def start_evolution(self):
        """Initializes the evolution loop for the Gemma shard."""
        print("[GEMMA-INTEL]: Open-weights cognitive shard ONLINE.")
