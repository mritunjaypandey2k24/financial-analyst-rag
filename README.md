# Financial Analyst RAG Project

This project implements a Retrieval-Augmented Generation (RAG) application designed specifically for analyzing financial documents. Users can upload financial reports, ask questions, and get specific insights or summaries using a document-aware AI agent.

## Project Overview
- **Document Upload:** Financial documents in PDF, CSV, and other formats can be uploaded.
- **RAG Pipeline:** Retrieval and generation pipeline utilizing pre-trained embedding models and open-source LLMs.
- **Agent Tasks:** Perform multiple tasks such as Q&A, summarization, and financial metric extraction.

## Project Structure
```
financial-analyst-rag/
├── notebooks/
│   ├── financial_analyst_rag.ipynb     # Google Colab-ready Jupyter notebook
├── data/
│   ├── test_docs/                     # Example financial documents for testing
├── models/
│   ├── embeddings/                    # Pre-trained embedding models config/scripts.
│   ├── llm/                           # LLM configuration (e.g., Falcon, Bloom, etc.)
├── utils/
│   ├── preprocessing.py               # Scripts for data extraction & cleaning
│   ├── retriever.py                   # Scripts for document retrieval
│   ├── agent_pipeline.py              # End-to-end pipeline setup
├── README.md                          # Project overview
├── requirements.txt                   # Python dependencies
└── .gitignore                         # Ignore unnecessary files
```

## How to Run
1. Clone the repository: `git clone https://github.com/mritunjaypandey2k24/financial-analyst-rag.git`
2. Open the notebook in Google Colab: `notebooks/financial_analyst_rag.ipynb`
3. Follow the steps in the notebook to upload documents and perform analysis.

## Dependencies
- `torch`, `transformers`, `sentence-transformers`, `faiss-cpu`
- `pandas`, `matplotlib`, `seaborn` (optional for visualization)

## Future Enhancements
- Multi-document analysis
- Advanced AI agent workflows for financial prediction

## License
[MIT License](LICENSE)