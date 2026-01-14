# Orchestrates the RAG pipeline: combines retriever and LLM.

from transformers import AutoTokenizer, AutoModelForCausalLM
from utils.retriever import DocumentRetriever
from typing import List
import torch

class FinancialRAGAgent:
    def __init__(self, llm_model_name: str = 'tiiuae/falcon-7b-instruct'):
        """Initialize the RAG agent with a retriever and LLM."""
        self.retriever = DocumentRetriever()
        self.tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
        self.model = AutoModelForCausalLM.from_pretrained(llm_model_name, device_map='auto')


    def answer_query(self, query: str, documents: List[str]) -> str:
        """Retrieve context and generate an answer."""
        embeddings = self.retriever.create_embeddings(documents)
        self.retriever.build_index(embeddings)
    
        # Retrieve relevant context
        context_indices = self.retriever.query(query)
        relevant_context = "".join([documents[i] for i in context_indices])
    
        # Truncate context to fit within max token length limits
        max_input_tokens = 2048  # Adjust based on model's maximum input length
        truncated_context = relevant_context[:max_input_tokens - len(query)]
    
        # Tokenize input and send it to appropriate device
        inputs = self.tokenizer(
            f'{truncated_context} Question: {query}',
            return_tensors='pt',
            truncation=True,  # Ensure tokenization itself respects token limits
        ).to('cuda' if torch.cuda.is_available() else 'cpu')
    
        # Generate output while restricting the number of new tokens
        outputs = self.model.generate(
            inputs['input_ids'],
            max_new_tokens=128,  # Focus on controlling output length
            pad_token_id=self.tokenizer.eos_token_id  # Avoid unexpected behavior for padding
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
