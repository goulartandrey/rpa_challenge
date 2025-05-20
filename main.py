import asyncio

from services.downloader import download_all_invoices
from services.scraper import scrape
from utils.utils import export_csv

URL="https://rpachallengeocr.azurewebsites.net/"

def main():
    """Main function to run the routine."""
    # start_time = time.time() # Remove comment to check time of execution
    invoices = scrape(URL)
    if invoices:
        asyncio.run(download_all_invoices(invoices))
        export_csv(invoices)
        print("Successfully downloaded.")
    else:
        print("No invoice found.")
    # print(f"Tempo de execução: {time.time() - start_time:.2f} segundos")  # Remove comment to check time of execution


if __name__ == "__main__":
    main()
