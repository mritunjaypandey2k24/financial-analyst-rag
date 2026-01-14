
import os
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

def extract_pdf_text(file_path: str) -> str:
    """
    Extract raw text from a PDF or HTML file with robust error handling.
    Supports both PDF and HTML formats.

    Args:
        file_path (str): Path to the file (HTML or PDF).

    Returns:
        str: Extracted text.
    """
    try:
        # Convert path to lowercase to avoid .HTML vs .html issues
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext == ".html" or file_ext == ".htm":
            # Handle HTML files
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
                # Check if the content is empty or whitespace
                if not content.strip():
                    return ""
                
                soup = BeautifulSoup(content, "html.parser")
                
                # Remove script and style elements
                for script_or_style in soup(["script", "style"]):
                    script_or_style.decompose()
                
                # Extract readable text
                text = soup.get_text(separator=' ')
                return " ".join(text.split())

        elif file_ext == ".pdf":
            # Handle PDF files
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
            return text
        
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

    except Exception as e:
        # Specific error message for better debugging
        raise RuntimeError(f"Error processing {os.path.basename(file_path)}: {e}")

def clean_text(text: str) -> str:
    """
    Simple cleaner to remove extra whitespace and newlines.

    Args:
        text (str): Raw text to clean.

    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""
    # Remove excessive newlines and tabs
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    # Remove multiple spaces
    return " ".join(text.split())
