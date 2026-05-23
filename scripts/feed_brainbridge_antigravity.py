import sys
import os

# Add root and backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.brain_bridge import BrainBridge
from backend.core.antigravity_bridge import AntigravityBridge

def main():
    print("--- SENTINELAI: BRAINBRIDGE INGESTION ENGINE ---")
    print("[*] Initializing Bridges...")
    
    brain = BrainBridge(db_path="vector_db")
    agy = AntigravityBridge()
    
    print("[*] Requesting knowledge synthesis from Antigravity CLI...")
    summary_res = agy.get_history_summary()
    
    if summary_res["status"] == "success":
        content = summary_res["data"]
        print("[+] Knowledge acquired. Ingesting into BrainBridge...")
        
        metadata = {
            "source": "Antigravity CLI History",
            "type": "architectural_synthesis",
            "version": "1.0.0"
        }
        
        success = brain.feed_brain(content, metadata)
        if success:
            print("[SUCCESS] BrainBridge updated with Antigravity intelligence.")
        else:
            print("[ERROR] Failed to commit knowledge to BrainBridge.")
    else:
        print(f"[ERROR] Knowledge acquisition failed: {summary_res['message']}")

if __name__ == "__main__":
    main()
