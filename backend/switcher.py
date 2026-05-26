from backend.core.local_ai import LocalIntelligence
from backend.core.hexstrike_client import HexstrikeEngine

class ModelSwitcher:
    """Manages the active intelligence engine for SpartanAI/Jarvis."""
    def __init__(self):
        self.available_engines = ['gemini', 'Jarvis', 'hexstrike', 'auto']
        self.current_engine = 'auto'
        self._Jarvis_instance = None
        self._hexstrike_instance = None

    def switch(self, engine_name):
        """Switches the active engine and ensures it is ready."""
        if engine_name not in self.available_engines:
            print(f"[ModelSwitcher] Error: Engine '{engine_name}' not supported.")
            return False
            
        print(f"[ModelSwitcher] Switching active intelligence to: {engine_name.upper()}")
        self.current_engine = engine_name
        
        # Immediate activation check
        if engine_name == 'Jarvis':
            self.get_Jarvis().ensure_service_active()
        elif engine_name == 'hexstrike':
            self.get_hexstrike().ensure_active()
            
        return True

    def get_current(self):
        """Returns the name of the currently active engine."""
        return self.current_engine

    def get_Jarvis(self):
        """Retrieves or initializes the LocalIntelligence (Jarvis) instance."""
        if not self._Jarvis_instance:
            self._Jarvis_instance = LocalIntelligence()
        return self._Jarvis_instance

    def get_hexstrike(self):
        """Retrieves or initializes the HexstrikeEngine instance."""
        if not self._hexstrike_instance:
            self._hexstrike_instance = HexstrikeEngine()
        return self._hexstrike_instance

    def route_query(self, query):
        """Autonomously determines the best engine for a given query."""
        query_lower = query.lower()
        
        # Offensive Intelligence Triggers (Hexstrike)
        offensive_keywords = ['nmap', 'recon', 'scan', 'exploit', 'vulnerability', 'cve', 'target', 'payload']
        if any(kw in query_lower for kw in offensive_keywords):
            return 'hexstrike'
            
        # Local Sovereign Intelligence Triggers (Jarvis/Brain)
        sovereign_keywords = ['local', 'brain', 'Jarvis', 'private', 'sovereign', 'internal', 'vault']
        if any(kw in query_lower for kw in sovereign_keywords):
            return 'Jarvis'
            
        # Default to Gemini for general reasoning and broad knowledge
        return 'gemini'

    def get_engine_for_query(self, query):
        """Returns the appropriate engine instance based on the query, if in 'auto' mode."""
        engine_name = self.current_engine
        if engine_name == 'auto':
            engine_name = self.route_query(query)
            
        if engine_name == 'Jarvis':
            return self.get_Jarvis()
        elif engine_name == 'hexstrike':
            return self.get_hexstrike()
        else:
            return None # Gemini handled by external uplink logic or specific handler
