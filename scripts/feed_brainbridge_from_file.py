import sys
import os

# Add root and backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.brain_bridge import BrainBridge

def main():
    print("--- SENTINELAI: BRAINBRIDGE FILE INGESTION ---")
    
    import sys
    file_path = sys.argv[1] if len(sys.argv) > 1 else ".gemini/antigravity-cli/scratch/monetization_summary.txt"
    
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return
        
    brain = BrainBridge(db_path="vector_db")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    print(f"[+] Ingesting {file_path} into BrainBridge...")
    
    metadata = {
        "source": "Antigravity CLI Synthesis",
        "type": "monetization_overview",
        "version": "1.0.0"
    }
    
    success = brain.feed_brain(content, metadata)
    if success:
        print("[SUCCESS] BrainBridge updated with monetization knowledge.")
    else:
        print("[ERROR] Ingestion failed.")

if __name__ == "__main__":
    main()
