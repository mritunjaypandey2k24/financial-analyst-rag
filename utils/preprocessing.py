# Script for data extraction and cleaning.
import pandas as pd
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
from typing import List

def extract_pdf_text(file_path: str) -> str:
    """
    Extract raw text from a PDF or HTML file.

    Args:
        file_path (str): Path to the file (PDF or HTML).

    Returns:
        str: Extracted text.
    """
    try:
        if file_path.endswith(".html"):
            # Handle HTML files
            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file.read(), "html.parser")
                return soup.get_text()
        elif file_path.endswith(".pdf"):
            # Handle PDF files
            reader = PdfReader(file_path)
            text = "".join([page.extract_text() for page in reader.pages])
            return text
        else:
            raise ValueError("Unsupported file type. Only PDF and HTML files are supported.")
    except Exception as e:
        raise RuntimeError(f"Error processing file {file_path}: {e}")

def clean_text(raw_text: str) -> str:
    """
    Clean raw text by removing unwanted characters.

    Args:
        raw_text (str): The raw text extracted from the document.

    Returns:
        str: Cleaned text.
    """
    return raw_text.replace('\n', ' ').replace('\t', ' ').strip()
