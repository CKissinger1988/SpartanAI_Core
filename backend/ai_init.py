import sys
import os
import time
import json
import logging

# Add paths for Jarvis and Jeeves
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'JarvisAI_Stable'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Jeeves-AI'))

from switcher import ModelSwitcher
from core.jarvis import Jarvis
from core.local_ai import LocalIntelligence
from core.hexstrike_client import HexstrikeEngine
from core.brain_bridge import BrainBridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AI_Init")

def initialize_ai_systems():
    logger.info("AI_INIT: Initializing Neural Connections...")
    
    # 1. Initialize Local Intelligence Engine (Ollama)
    logger.info("AI_INIT: Verifying Local Intelligence Core (Ollama)...")
    try:
        local_intel = LocalIntelligence()
        if not local_intel.ensure_service_active():
            logger.error("AI_INIT: Local Intelligence Core failed to initialize.")
            return False
        logger.info("AI_INIT: Local Intelligence Core ONLINE.")
    except Exception as e:
        logger.error(f"AI_INIT: ERROR during Local Intelligence initialization: {e}")
        return False

    # 2. Initialize Offensive Intelligence (Hexstrike)
    logger.info("AI_INIT: Verifying Offensive Intelligence Core (Hexstrike)...")
    try:
        hexstrike = HexstrikeEngine()
        if not hexstrike.ensure_active():
            logger.warning("AI_INIT: Offensive Intelligence Core (Hexstrike) is OFFLINE. Proceeding with caution.")
        else:
            logger.info("AI_INIT: Offensive Intelligence Core ONLINE.")
    except Exception as e:
        logger.error(f"AI_INIT: ERROR during Hexstrike initialization: {e}")

    # 3. Initialize BrainBridge (Vector DB)
    logger.info("AI_INIT: Verifying BrainBridge Connectivity...")
    try:
        brain = BrainBridge()
        if not brain.client:
            logger.warning("AI_INIT: BrainBridge vector database not found at default path. Local RAG will be unavailable.")
        else:
            logger.info("AI_INIT: BrainBridge CONNECTED.")
    except Exception as e:
        logger.error(f"AI_INIT: ERROR during BrainBridge initialization: {e}")

    # 4. Initialize Jarvis Supreme AI
    logger.info("AI_INIT: Awakening Jarvis Supreme AI...")
    try:
        jarvis = Jarvis()
        jarvis.greet()
    except Exception as e:
        logger.error(f"AI_INIT: ERROR during Jarvis awakening: {e}")
        return False

    logger.info("AI_INIT: ALL NEURAL CONNECTIONS AND DEEP LEARNING SYSTEMS INITIALIZED.")
    return True

if __name__ == "__main__":
    if initialize_ai_systems():
        sys.exit(0)
    else:
        sys.exit(1)
