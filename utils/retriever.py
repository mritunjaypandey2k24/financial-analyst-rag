# Utility script for document retrieval and FAISS-based similarity search.

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List

class DocumentRetriever:
    def __init__(self, embedding_model_name: str = 'sentence-transformers/all-mpnet-base-v2'):
        """Initialize retriever with FAISS index and embedding model."""
        self.model = SentenceTransformer(embedding_model_name)
        self.index = None

    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts."""
        return self.model.encode(texts, show_progress_bar=True)

    def build_index(self, vectors: np.ndarray):
        """Build a FAISS similarity index."""
        self.index = faiss.IndexFlatL2(vectors.shape[1])
        self.index.add(vectors)

    def query(self, query_text: str, top_k: int = 5) -> List[int]:
        """Retrieve the top-k most similar documents for a query."""
        query_vector = self.model.encode([query_text])
        distances, indices = self.index.search(query_vector, top_k)
        return indices.flatten().tolist()