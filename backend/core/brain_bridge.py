import chromadb
import os

class BrainBridge:
    """Connects Jarvis logic directly to the deep learning vector brain (ChromaDB)."""
    def __init__(self, db_path="vector_db"):
        self.db_path = db_path
        if os.path.exists(db_path):
            self.client = chromadb.PersistentClient(path=db_path)
        else:
            self.client = None

    def get_tactical_context(self, query, n_results=3):
        """Retrieves related tactical knowledge from the brain."""
        if not self.client:
            return "No brain data available."
        
        try:
            # List collections to find the active one
            collections = self.client.list_collections()
            if not collections:
                return "Brain is empty."
            
            # Using the first collection for tactical context
            collection = self.client.get_collection(collections[0].name)
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            context = "\n".join([str(doc) for doc in results['documents'][0]])
            return context
        except Exception as e:
            return f"Error feeding from brain: {e}"

    def feed_brain(self, content, metadata=None):
        """Commits new knowledge to the permanent brain memory."""
        if not self.client:
            return False
            
        try:
            collections = self.client.list_collections()
            if not collections:
                collection = self.client.create_collection("nexus_brain")
            else:
                collection = self.client.get_collection(collections[0].name)
                
            import uuid
            collection.add(
                documents=[content],
                metadatas=[metadata or {"source": "jarvis_deep_learning"}],
                ids=[str(uuid.uuid4())]
            )
            return True
        except Exception as e:
            print(f"Brain feed error: {e}")
            return False
