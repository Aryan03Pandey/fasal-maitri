import faiss
import numpy as np
from typing import List, Tuple
from .web_search import web_search
from .embedding import get_embedding

class RAGService:
    def __init__(self):
        self.dimension = 768  # IndicBERT embedding dimension
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []

    def add_texts(self, texts: List[str]):
        """Add texts to the vector store"""
        if not texts:
            return
        
        embeddings = []
        for text in texts:
            embedding = get_embedding(text).numpy()
            embeddings.append(embedding)
            self.texts.append(text)
            
        embeddings_array = np.array(embeddings).astype('float32')
        self.index.add(embeddings_array)

    def search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        """Search most similar texts for a query"""
        query_embedding = get_embedding(query).numpy().astype('float32').reshape(1, -1)
        D, I = self.index.search(query_embedding, k)
        
        results = []
        for idx, distance in zip(I[0], D[0]):
            if idx >= 0 and idx < len(self.texts):
                results.append((self.texts[idx], float(distance)))
        return results

    async def query(self, user_query: str) -> str:
        """Full RAG pipeline"""
        # 1. Get relevant web search results
        search_results = web_search(user_query, max_results=3)
        
        # 2. Add to vector store
        self.add_texts(search_results)
        
        # 3. Find most relevant passages
        similar_texts = self.search(user_query, k=2)
        
        # 4. Format context
        context = "\n".join([text for text, _ in similar_texts])
        
        return context