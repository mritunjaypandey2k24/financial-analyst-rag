# Utility script for document extraction and data cleaning.

import pandas as pd
from PyPDF2 import PdfReader
from typing import List

def extract_pdf_text(file_path: str) -> str:
    """Extract raw text from a PDF file."""
    reader = PdfReader(file_path)
    text = "".join([page.extract_text() for page in reader.pages])
    return text


def extract_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)


def clean_text(raw_text: str) -> str:
    """Clean raw text by removing unwanted characters."""
    return raw_text.replace('\n', ' ').replace('\t', ' ').strip()