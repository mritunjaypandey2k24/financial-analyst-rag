import os
import requests

def fetch_sec_filings(ticker: str, filing_type: str, save_directory: str, num_filings: int = 5):
    """
    Fetch financial filings (e.g., 10-K, 10-Q) for a given company ticker symbol from the SEC EDGAR database.

    Args:
        ticker (str): The CENTRAL INDEX KEY (CIK) or stock ticker symbol (e.g., 'AAPL', 'MSFT').
        filing_type (str): Type of filing to fetch (e.g., '10-K', '10-Q').
        save_directory (str): Directory to save fetched filings.
        num_filings (int): Number of filings to download (default: 5).
    """
    # Ensure the save directory exists
    os.makedirs(save_directory, exist_ok=True)

    # SEC User-Agent header (required by EDGAR system)
    headers = {
        "User-Agent": "Your Name <your-email@example.com>",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.sec.gov"
    }

    # EDGAR base endpoint for fetching CIK filings
    base_url = f"https://data.sec.gov/submissions/CIK{ticker}.json"

    print(f"Fetching company filings for CIK '{ticker}'...")
    response = requests.get(base_url, headers=headers)

    if response.status_code != 200:
        print(f"Unable to retrieve data for CIK {ticker}: HTTP {response.status_code}")
        return

    company_data = response.json()

    # Access lists of recent filings
    if "filings" not in company_data or "recent" not in company_data["filings"]:
        print(f"Filings not found for CIK '{ticker}'.")
        return

    accessions = company_data["filings"]["recent"]["accessionNumber"]
    form_types = company_data["filings"]["recent"]["form"]

    # Filter filings by type (e.g., '10-K', '10-Q')
    matching_filings = [
        acc for acc, form in zip(accessions, form_types) if form == filing_type
    ]

    if not matching_filings:
        print(f"No {filing_type} filings found for CIK '{ticker}'.")
        return

    # Limit the number of fetched filings
    matching_filings = matching_filings[:num_filings]

    # Download and save each filing
    for accession in matching_filings:
        filing_url = f"https://www.sec.gov/Archives/edgar/data/{ticker}/{accession.replace('-', '')}/{accession}-index.htm"
        print(f"Downloading filing: {filing_url}")

        filing_response = requests.get(filing_url, headers=headers)
        if filing_response.status_code == 200:
            file_path = os.path.join(save_directory, f"{accession}.html")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(filing_response.text)
            print(f"Saved filing to {file_path}")
        else:
            print(f"Failed to download filing {accession}: HTTP {filing_response.status_code}")

    print(f"Successfully downloaded {len(matching_filings)} filings of type {filing_type} for CIK '{ticker}'.")

# Example usage
if __name__ == "__main__":
    fetch_sec_filings(
        ticker="0000320193",  # CIK for Apple Inc.
        filing_type="10-K",   # Fetch Annual Reports
        save_directory="data/sec_filings/",
        num_filings=3         # Number of filings to fetch
    )
