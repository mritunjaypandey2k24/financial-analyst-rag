# Root-level preprocessing script for high-level preprocessing workflows
from utils.preprocessing import extract_pdf_text, clean_text

def preprocess_file(file_path: str) -> str:
    """
    High-level function to preprocess a single file by extracting
    and cleaning its content.

    Args:
        file_path (str): Path to the file (HTML or PDF).

    Returns:
        str: Cleaned text.
    """
    raw_text = extract_pdf_text(file_path)  # Call utility function
    return clean_text(raw_text)            # Call cleaning function
