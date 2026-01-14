# Orchestrates the RAG pipeline: combines retriever and LLM.

from transformers import AutoTokenizer, AutoModelForCausalLM
from utils.retriever import DocumentRetriever
from typing import List
import torch
import re

class FinancialRAGAgent:
    def __init__(self, llm_model_name: str = 'tiiuae/falcon-7b-instruct'):
        """Initialize the RAG agent with a retriever and LLM."""
        self.retriever = DocumentRetriever()
        self.tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
        self.model = AutoModelForCausalLM.from_pretrained(llm_model_name, device_map='auto')


    def answer_query(self, query: str, documents: List[str]) -> str:
        """Retrieve context and generate a clean and concise answer."""
        embeddings = self.retriever.create_embeddings(documents)
        self.retriever.build_index(embeddings)
    
        # Retrieve relevant context
        context_indices = self.retriever.query(query)
        relevant_context = "".join([documents[i] for i in context_indices])
    
        # Truncate input to respect token limits
        max_input_tokens = 2048
        truncated_context = relevant_context[:max_input_tokens - len(query)]
    
        # Tokenize input and send it to appropriate device
        inputs = self.tokenizer(
            f'{truncated_context} Question: {query}',
            return_tensors='pt',
            truncation=True,  # Ensure tokenization itself respects token limits
            padding=True,  # Add padding to align input sequence
            max_length=max_input_tokens  # Define maximum input length explicitly
        ).to('cuda' if torch.cuda.is_available() else 'cpu')
    
        # Generate output while restricting the number of new tokens
        outputs = self.model.generate(
            inputs['input_ids'],
            max_new_tokens=128,  # Specify output length
            pad_token_id=self.tokenizer.eos_token_id  # Explicitly set padding token
        )
    
        # Decode and clean the model's output
        raw_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
        # Regex to clean unwanted metadata and noise
        cleaned_output = re.sub(r"http.*? ", "", raw_output)  # Remove URLs
        cleaned_output = re.sub(r"[\s]+", " ", cleaned_output.strip())  # Remove extra spaces
        return cleaned_output
