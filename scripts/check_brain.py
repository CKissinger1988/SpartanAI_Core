import chromadb
import os

def check_brain():
    try:
        db_path = r"C:\GitHub\SpartanAI_Core\backend\vector_db"
        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_or_create_collection(name="spartanai_security_core_brain")
        
        count = collection.count()
        print(f"TOTAL ASSIMILATED PATHWAYS (Memories): {count}")
        
        if count > 0:
            print("\n--- RECENTLY INGESTED INTELLIGENCE ---")
            results = collection.peek(limit=5)
            for i, doc in enumerate(results['documents']):
                meta = results['metadatas'][i] if results['metadatas'] else "No Meta"
                print(f"[{meta}] -> {doc[:150]}...")
    except Exception as e:
        print(f"Error accessing BrainBridge: {e}")

if __name__ == "__main__":
    check_brain()
