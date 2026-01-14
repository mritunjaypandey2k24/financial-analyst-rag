# Orchestrates the RAG pipeline: combines retriever and LLM.

from transformers import AutoTokenizer, AutoModelForCausalLM
from utils.retriever import DocumentRetriever

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
    
    context_indices = self.retriever.query(query)
    relevant_context = "".join([documents[i] for i in context_indices])
    
    # Truncate the context to fit the model's max length
    max_context_length = 2000  # Reasonable buffer below 2048
    truncated_context = relevant_context[:max_context_length]

    inputs = self.tokenizer(
        f'{truncated_context} Question: {query}', return_tensors='pt'
    ).to('cuda' if torch.cuda.is_available() else 'cpu')
    outputs = self.model.generate(inputs['input_ids'], max_length=512)
    return self.tokenizer.decode(outputs[0])
