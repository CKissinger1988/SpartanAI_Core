import chromadb
import sys
import os

def check_jarvis_memory():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'vector_db')
    try:
        client = chromadb.PersistentClient(path=db_path)
        collections = client.list_collections()
        
        print("=== JARVIS NEURAL MEMORY AUDIT ===")
        if not collections:
            print("No memory shards found. Jarvis memory is empty.")
            return
            
        total_memories = 0
        for collection in collections:
            count = collection.count()
            total_memories += count
            print(f"Collection: {collection.name}")
            print(f" - Memories stored: {count}")
            
            # Print a sample memory if it exists
            if count > 0:
                sample = collection.peek(limit=1)
                print(f" - Sample Memory Fragment:")
                if sample['documents'] and len(sample['documents']) > 0:
                    doc = sample['documents'][0][:200] + "..." if len(sample['documents'][0]) > 200 else sample['documents'][0]
                    print(f"   \"{doc}\"")
                print("-" * 40)
                
        print(f"\nTOTAL NEURAL PATHWAYS ASSIMILATED: {total_memories}")
        
    except Exception as e:
        print(f"Error accessing neural memory: {e}")

if __name__ == "__main__":
    check_jarvis_memory()
