# Script for document retrieval and FAISS-based similarity search.

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class DocumentRetriever:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize the retriever with a sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        self.index = None

    def create_embeddings(self, documents: list) -> np.ndarray:
        """
        Create embeddings for the provided documents.
        
        Args:
            documents (list): List of document strings to create embeddings for.
        
        Returns:
            np.ndarray: Numpy array of document embeddings.
        """
        if not documents:
            raise ValueError("No documents provided to create embeddings.")
        return np.array(self.model.encode(documents, show_progress_bar=True))

    def build_index(self, embeddings: np.ndarray):
        """
        Build a FAISS index from embeddings.
        
        Args:
            embeddings (np.ndarray): Array of document embeddings.
        """
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def query(self, query: str, k: int = 5) -> list:
        """
        Query the FAISS index to retrieve the top-k relevant documents.
        
        Args:
            query (str): The query string.
            k (int): Number of top documents to retrieve.
        
        Returns:
            list: Indices of the most relevant documents.
        """
        if self.index is None:
            raise ValueError("FAISS index has not been built. Call build_index() first.")
        
        # Create an embedding for the query.
        query_embedding = self.model.encode([query])
        
        # Search the index and return top-k results.
        distances, indices = self.index.search(np.array(query_embedding), k)
        return indices.flatten().tolist()
