import os
import uuid

try:
    import chromadb
except ImportError:
    chromadb = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class BrainBridge:
    """Connects Jarvis logic to ChromaDB and the Gemini AI Cognitive Core."""
    def __init__(self, db_path="vector_db"):
        self.db_path = db_path
        self.collection_name = os.environ.get("BRAINBRIDGE_COLLECTION", "nexus_brain")
        self.client = None
        if chromadb:
            os.makedirs(db_path, exist_ok=True)
            self.client = chromadb.PersistentClient(path=db_path)
        self.status = "OFFLINE"
        self.light_status = "INACTIVE" # Primary knowledge
        self.shadow_status = "INACTIVE" # Fallback/harvested knowledge
        
        # Initialize Gemini API with sovereign fallback
        self._init_generative_core()

    def _init_generative_core(self):
        if genai is None:
            self.status = "LOCAL_KNOWLEDGE_ONLY"
            self.light_status = "VECTOR_DB_ACTIVE" if self.client else "DEPENDENCY_MISSING"
            return

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key or "DUMMY" in api_key:
            self.status = "LOCAL_KNOWLEDGE_ONLY"
            self.light_status = "VECTOR_DB_ACTIVE" if self.client else "DEPENDENCY_MISSING"
            return
        
        try:
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
            self.status = "ONLINE"
            self.light_status = "ACTIVE"
        except Exception as e:
            self.status = f"CONFIG_ERROR: {e}"
            self.light_status = "ERROR"

    def get_tactical_context(self, query, n_results=3):
        """Retrieves related tactical knowledge from the brain."""
        if not self.client:
            return "No brain data available."
        
        try:
            # List collections to find the active one
            collections = self.client.list_collections()
            if not collections:
                return "Brain is empty."
            
            collection = self.client.get_collection(self.collection_name)
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            context = "\n".join([str(doc) for doc in results['documents'][0]])
            return context
        except Exception as e:
            return f"Error feeding from brain: {e}"

    def analyze_with_gemini(self, prompt, use_context=True):
        """Uses Gemini AI to analyze a prompt, optionally enriched with vector brain context."""
        try:
            full_prompt = prompt
            if use_context:
                context = self.get_tactical_context(prompt)
                full_prompt = f"Context from Supreme AI Brain:\n{context}\n\nOperator Prompt: {prompt}"
            
            if not hasattr(self, 'gemini_model'):
                return "[GEMINI_ERROR]: Cognitive generation failed - API key not set or local fallback active."
            
            response = self.gemini_model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"[GEMINI_ERROR]: Cognitive generation failed - {str(e)}"

    def feed_brain(self, content, metadata=None):
        """Commits new knowledge to the permanent brain memory."""
        if not self.client:
            return False
            
        try:
            collections = self.client.list_collections()
            if not collections:
                collection = self.client.get_or_create_collection(self.collection_name)
            else:
                collection = self.client.get_or_create_collection(self.collection_name)
                
            collection.add(
                documents=[content],
                metadatas=[metadata or {"source": "jarvis_deep_learning"}],
                ids=[str(uuid.uuid4())]
            )
            return True
        except Exception as e:
            print(f"Brain feed error: {e}")
            return False
