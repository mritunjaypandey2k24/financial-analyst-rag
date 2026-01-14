import os
import requests
import time

def fetch_sec_filings(ticker: str, filing_type: str, save_directory: str, num_filings: int = 5):
    # 1. Ensure CIK is a 10-digit string
    # This turns "320193" into "0000320193"
    cik = str(ticker).zfill(10)
    
    os.makedirs(save_directory, exist_ok=True)

    # 2. SEC REQUIRES a specific User-Agent format: "Name email@address.com"
    headers = {
        "User-Agent": "Mritunjay Pandey mritunjaypandey.ee@gmail.com", 
        "Accept-Encoding": "gzip, deflate",
        "Host": "data.sec.gov"
    }

    # The API endpoint
    base_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    
    print(f"Requesting: {base_url}")

    try:
        response = requests.get(base_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: Received HTTP {response.status_code} for CIK {cik}")
            if response.status_code == 404:
                print("Hint: Check if the CIK is correct or if the SEC server is blocking the request.")
            return

        company_data = response.json()
        recent = company_data.get("filings", {}).get("recent", {})
        
        if not recent:
            print(f"No recent filings found for {ticker}")
            return

        # Filter filings
        accessions = recent.get("accessionNumber", [])
        forms = recent.get("form", [])
        primary_docs = recent.get("primaryDocument", [])

        count = 0
        for i in range(len(forms)):
            if forms[i] == filing_type and count < num_filings:
                acc = accessions[i]
                acc_clean = acc.replace("-", "")
                doc_name = primary_docs[i]
                
                # Construct the download URL for the actual document
                # Format: https://www.sec.gov/Archives/edgar/data/{cik_no_zeros}/{acc_clean}/{doc_name}
                # Note: For the Archives path, the CIK often has leading zeros removed
                cik_stripped = cik.lstrip('0')
                download_url = f"https://www.sec.gov/Archives/edgar/data/{cik_stripped}/{acc_clean}/{doc_name}"
                
                print(f"Downloading: {download_url}")
                
                # Respect SEC rate limits
                time.sleep(0.1)
                
                file_resp = requests.get(download_url, headers={"User-Agent": headers["User-Agent"]})
                if file_resp.status_code == 200:
                    save_path = os.path.join(save_directory, f"{acc}.html")
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(file_resp.text)
                    count += 1
                else:
                    print(f"Failed to download document: {file_resp.status_code}")

        print(f"Done! Downloaded {count} filings for {ticker}.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
