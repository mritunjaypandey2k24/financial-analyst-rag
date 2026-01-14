import os
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

def extract_text(file_path: str) -> str:
    """
    Extract clean, human-readable text from SEC iXBRL (HTML) or PDF.
    """
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext in [".html", ".htm"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                
                # 1. REMOVE SYSTEM/META DATA: 
                # This removes the huge block of XML/XBRL metadata at the top 
                # that isn't part of the actual report text.
                for meta in soup(["ix:header", "ix:hidden", "style", "script"]):
                    meta.decompose()

                # 2. EXTRACT TEXT WITH SEPARATOR:
                # separator=' ' prevents words from being mashed together 
                # when removing table cells (e.g., "Total""$100" -> "Total $100")
                raw_text = soup.get_text(separator=' ')
                
                return clean_text(raw_text)

        elif file_ext == ".pdf":
            reader = PdfReader(file_path)
            text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            return clean_text(text)
            
        else:
            print(f"Skipping unsupported file: {file_path}")
            return ""

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return ""

def clean_text(text: str) -> str:
    """
    Standardizes whitespace for better RAG performance.
    """
    if not text:
        return ""
    # Remove extra whitespace and newlines
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return " ".join(chunk for chunk in chunks if chunk)
