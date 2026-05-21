# Dummy file to satisfy import dependency

from backend.core.local_ai import LocalIntelligence
from backend.core.hexstrike_client import HexstrikeEngine

class ModelSwitcher:
    def __init__(self):
        self.available_engines = ['gemini', 'nexus', 'hexstrike', 'auto']
        self.current_engine = 'auto'
        self._nexus_instance = None
        self._hexstrike_instance = None

    def switch(self, engine_name):
        if engine_name not in self.available_engines:
            print(f"[ModelSwitcher] Error: Engine '{engine_name}' not supported. Defaulting to 'auto'.")
            self.current_engine = 'auto'
            return False
            
        print(f"[ModelSwitcher] Switching active intelligence to: {engine_name.upper()}")
        self.current_engine = engine_name
        
        # Immediate activation check
        if engine_name == 'nexus':
            self.get_nexus().ensure_service_active()
        elif engine_name == 'hexstrike':
            self.get_hexstrike().ensure_active()
            
        return True

    def get_nexus(self):
        if not self._nexus_instance:
            self._nexus_instance = LocalIntelligence()
        return self._nexus_instance

    def get_hexstrike(self):
        if not self._hexstrike_instance:
            self._hexstrike_instance = HexstrikeEngine()
        return self._hexstrike_instance

    def get_current(self):
        return self.current_engine
