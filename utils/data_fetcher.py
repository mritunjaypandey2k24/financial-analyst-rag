import os
import requests
from typing import List


def fetch_sec_filings(ticker: str, filing_type: str, save_directory: str, num_filings: int = 10):
    """
    Fetch financial filings (e.g., 10-K, 10-Q) for a given company ticker symbol from the SEC EDGAR database.

    Args:
        ticker (str): The stock ticker symbol of the company (e.g., 'AAPL', 'TSLA').
        filing_type (str): Type of filing to fetch (e.g., '10-K', '10-Q').
        save_directory (str): Directory to save fetched filings.
        num_filings (int): The number of filings to download (default: 10).
    """
    # Ensure the save directory exists
    os.makedirs(save_directory, exist_ok=True)

    # User-Agent header for SEC EDGAR requests (standard requirement)
    headers = {
        "User-Agent": "Your Name <your-email@example.com>",  # Update this with your details
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.sec.gov"
    }

    # Base SEC EDGAR URL for fetching company submissions
    base_url = f"https://data.sec.gov/submissions/CIK{ticker}.json"

    # Retrieve company data
    print(f"Fetching company data for ticker '{ticker}'...")
    response = requests.get(base_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data for ticker {ticker}: HTTP {response.status_code}")
        return

    company_data = response.json()

    if "filings" not in company_data or "recent" not in company_data["filings"]:
        print(f"No filings found for ticker {ticker}.")
        return

    recent_filings = company_data["filings"]["recent"]
    accessions = recent_filings["accessionNumber"]
    form_types = recent_filings["form"]

    # Select filings of the specified type
    matching_filings = [accession for accession, form in zip(accessions, form_types) if form == filing_type]

    if not matching_filings:
        print(f"No {filing_type} filings found for ticker {ticker}.")
        return

    # Limit to requested number of filings
    matching_filings = matching_filings[:num_filings]

    # Fetch and save each filing
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

    print(f"Completed downloading {len(matching_filings)} filings for ticker '{ticker}'.")


if __name__ == "__main__":
    # Example usage
    # Fetch 10-K (Annual Reports) filings for Apple Inc. ('AAPL')
    fetch_sec_filings(ticker="0000320193", filing_type="10-K", save_directory="data/sec_filings")
