import os
import requests
import time

def fetch_sec_filings(ticker: str, filing_type: str, save_directory: str, num_filings: int = 5):
    # 1. Pad CIK to 10 digits
    cik = str(ticker).zfill(10)
    os.makedirs(save_directory, exist_ok=True)

    headers = {
        "User-Agent": "Mritunjay Pandey <mritunjaypandey.ee@gmail.com>", # Use your verified info
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.sec.gov"
    }

    # API endpoint for company metadata
    base_url = f"https://data.sec.gov/submissions/CIK{cik}.json"

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        company_data = response.json()
        
        recent_filings = company_data["filings"]["recent"]
        
        # Filter for matching filing types
        matches = []
        for i, form in enumerate(recent_filings["form"]):
            if form == filing_type:
                matches.append({
                    "accession": recent_filings["accessionNumber"][i],
                    "filename": recent_filings["primaryDocument"][i]
                })
            if len(matches) >= num_filings:
                break

        for item in matches:
            accession_raw = item["accession"]
            accession_clean = accession_raw.replace("-", "")
            primary_doc = item["filename"]

            # Construct URL for the ACTUAL document (HTM format)
            document_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_clean}/{primary_doc}"
            
            print(f"Downloading {filing_type}: {document_url}")
            
            # SEC Rate limit: 10 requests per second. Adding a small sleep is safer for bulk.
            time.sleep(0.1) 
            
            doc_response = requests.get(document_url, headers=headers)
            if doc_response.status_code == 200:
                # Save as .html for better parsing later
                file_path = os.path.join(save_directory, f"{accession_raw}.html")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(doc_response.text)
                print(f"Successfully saved to {file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Your loop logic remains correct!
