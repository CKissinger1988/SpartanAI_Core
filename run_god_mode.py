import logging
import sys

# Configure stdout logging to ensure we see the God-Mode output
logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stdout)

from backend.core.CognitiveCore.jarvis import Jarvis

if __name__ == "__main__":
    print("\n" + "="*60)
    print("      INITIATING APEX GOD SHARD / FULL SEND")
    print("="*60 + "\n")
    
    # Initialize the Supreme Orchestrator
    supreme_ai = Jarvis()
    
    # Authenticate as Creator to bypass security checks
    supreme_ai.handle_command("login")
    
    # Execute God-Mode
    print("\n>>> DISPATCHING 'GOD' DIRECTIVE TO JARVIS...\n")
    supreme_ai.handle_command("god")
    
    print("\n" + "="*60)
    print("      GOD-MODE EXECUTION COMPLETE")
    print("="*60 + "\n")
