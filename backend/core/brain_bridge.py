import os
import uuid
import logging

try:
    import chromadb
except ImportError:
    chromadb = None

# Support both the new google-genai and the deprecated google-generativeai
try:
    from google import genai
    from google.genai import types
    NEW_GENAI_AVAILABLE = True
except ImportError:
    try:
        import google.generativeai as genai_legacy
        NEW_GENAI_AVAILABLE = False
    except ImportError:
        genai_legacy = None
        NEW_GENAI_AVAILABLE = False

class BrainBridge:
    """Connects Jarvis logic to ChromaDB and the Gemini AI Cognitive Core."""
    def __init__(self, db_path="vector_db"):
        self.db_path = db_path
        self.collection_name = os.environ.get("BRAINBRIDGE_COLLECTION", "spartanai_security_core_brain")
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
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key or "DUMMY" in api_key:
            self.status = "LOCAL_KNOWLEDGE_ONLY"
            self.light_status = "VECTOR_DB_ACTIVE" if self.client else "DEPENDENCY_MISSING"
            return
        
        try:
            if NEW_GENAI_AVAILABLE:
                self.client_genai = genai.Client(api_key=api_key)
                self.gemini_model_name = 'gemini-1.5-pro'
                self.status = "ONLINE (NEW-SDK)"
            else:
                if genai_legacy is None:
                    self.status = "LOCAL_KNOWLEDGE_ONLY"
                    return
                genai_legacy.configure(api_key=api_key)
                self.gemini_model = genai_legacy.GenerativeModel('gemini-1.5-pro')
                self.status = "ONLINE (LEGACY-SDK)"
            
            self.light_status = "ACTIVE"
        except Exception as e:
            self.status = f"CONFIG_ERROR: {e}"
            self.light_status = "ERROR"

    def get_tactical_context(self, query, n_results=3, cortex_type="Questionable"):
        """Retrieves related tactical knowledge, filtered by cortex type."""
        if not self.client:
            return "No brain data available."
        
        try:
            collection = self.client.get_collection(self.collection_name)
            results = collection.query(
                query_texts=[query],
                n_results=n_results,
                where={"cortex": cortex_type}
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
            
            if NEW_GENAI_AVAILABLE and hasattr(self, 'client_genai'):
                response = self.client_genai.models.generate_content(
                    model=self.gemini_model_name,
                    contents=full_prompt
                )
                return response.text
            elif hasattr(self, 'gemini_model'):
                response = self.gemini_model.generate_content(full_prompt)
                return response.text
            else:
                return "[GEMINI_ERROR]: Cognitive generation failed - API key not set or local fallback active."
        except Exception as e:
            return f"[GEMINI_ERROR]: Cognitive generation failed - {str(e)}"

    def feed_brain(self, content, metadata=None, cortex_type="Questionable"):
        """Commits new knowledge to the permanent brain memory with cortex classification."""
        if not self.client:
            return False
            
        try:
            collection = self.client.get_or_create_collection(self.collection_name)
            
            meta = metadata or {"source": "jarvis_deep_learning"}
            meta["cortex"] = cortex_type
                
            collection.add(
                documents=[content],
                metadatas=[meta],
                ids=[str(uuid.uuid4())]
            )
            return True
        except Exception as e:
            print(f"Brain feed error: {e}")
            return False
