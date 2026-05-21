# Dummy file to satisfy import dependency

class ModelSwitcher:
    def __init__(self):
        self.available_engines = ['gemini', 'nexus', 'auto']
        self.current_engine = 'auto'

    def switch(self, engine_name):
        if engine_name not in self.available_engines:
            print(f"[ModelSwitcher] Error: Engine '{engine_name}' not supported. Defaulting to 'auto'.")
            self.current_engine = 'auto'
            return False
            
        print(f"[ModelSwitcher] Switching active intelligence to: {engine_name.upper()}")
        self.current_engine = engine_name
        return True

    def get_current(self):
        return self.current_engine
