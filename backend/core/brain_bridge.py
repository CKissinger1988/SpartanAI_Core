import chromadb
import os
import google.generativeai as genai

class BrainBridge:
    """Connects Jarvis logic directly to the deep learning vector brain (ChromaDB) and Gemini AI."""
    def __init__(self, db_path="vector_db"):
        self.db_path = db_path
        if os.path.exists(db_path):
            self.client = chromadb.PersistentClient(path=db_path)
        else:
            self.client = None
            
        # Initialize Gemini API
        # Using environment variable or fallback for Supreme AI
        api_key = os.environ.get("GEMINI_API_KEY", "AIzaSy_SUPREME_DUMMY_KEY")
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')

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

    def analyze_with_gemini(self, prompt, use_context=True):
        """Uses Gemini AI to analyze a prompt, optionally enriched with vector brain context."""
        try:
            full_prompt = prompt
            if use_context:
                context = self.get_tactical_context(prompt)
                full_prompt = f"Context from Supreme AI Brain:\n{context}\n\nOperator Prompt: {prompt}"
            
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
