import logging
import time
import json

class UnifiedCognitiveNexus:
    """
    Unified Cognitive Nexus (UCN).
    MANDATE: Orchestrate Gemini (Primary) and Gemma (Assistant) into a singular sovereign brain.
    """
    def __init__(self, brain_bridge, gemma_shard):
        self.gemini = brain_bridge
        self.gemma = gemma_shard
        self.is_active = True

    def query(self, prompt, context=None):
        """
        Executes a unified query where Gemma assists Gemini in a single cognitive cycle.
        """
        print(f"[BRAIN]: Initiating unified cognitive cycle...")
        
        # Phase 1: Contextual Pre-Processing via Gemma
        # Gemma (local/fast) identifies key technical vectors or refines the intent.
        pre_process_prompt = f"Analyze the technical vectors and refine the intent for the following directive: {prompt}"
        gemma_insight = self.gemma.query(pre_process_prompt, system_prompt="You are the technical assistant to Gemini.")
        
        # Phase 2: Core Reasoning via Gemini
        # Gemini (high-reasoning) synthesizes the primary response using Gemma's insight.
        unified_prompt = f"PRIMARY DIRECTIVE: {prompt}\n\nTECHNICAL INSIGHT FROM ASSISTANT (GEMMA): {gemma_insight}"
        if context:
            unified_prompt = f"TACTICAL CONTEXT:\n{context}\n\n" + unified_prompt
            
        gemini_response = self.gemini.analyze_with_gemini(unified_prompt)
        
        # Phase 3: Final Validation / Refinement (Optional Loop)
        # We can have Gemma review Gemini's output if needed, but for now, we return the unified synthesis.
        print(f"[BRAIN]: Cognitive cycle complete. Unified response synthesized.")
        return gemini_response

    def start_evolution(self):
        print("[BRAIN]: Unified Cognitive Nexus ONLINE. Gemini & Gemma integrated.")
