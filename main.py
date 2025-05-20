import asyncio
from datetime import datetime
import os
import time
from typing import List

import pandas as pd
import aiohttp
import aiofiles
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from schema import InvoiceSchema

load_dotenv()

# ENV variables
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH") or "./chromedriver"
URL = os.getenv("URL")
env_dir = os.getenv("INVOICES_DIR", "").strip()
INVOICES_DIR = os.path.join(env_dir, "invoices") if env_dir else "invoices"


def scrape(url: str) -> List[InvoiceSchema]:
    """Scrape URL data."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(
        CHROME_DRIVER_PATH), options=options)
    wait = WebDriverWait(driver, 5)

    invoices: List[InvoiceSchema] = []

    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.ID, "tableSandbox")))

        while True:
            table = driver.find_element(By.ID, "tableSandbox")
            rows = table.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if not cells:
                    continue

                try:
                    invoice = InvoiceSchema(
                        id=cells[1].text.strip(),
                        due_date=cells[2].text.strip(),
                        url=cells[3].find_element(
                            By.TAG_NAME, "a").get_attribute("href").strip()
                    )
                    invoices.append(invoice)
                except Exception as e:
                    print(f"Error: {e}")
                    continue

            try:
                next_button = driver.find_element(By.ID, "tableSandbox_next")
                if 'disabled' in next_button.get_attribute("class"):
                    break
                next_button.click()
                wait.until(EC.presence_of_element_located(
                    (By.ID, "tableSandbox")))
            except Exception:
                break

    finally:
        driver.quit()

    return invoices


def filter_invoices_by_due_date(data: List[InvoiceSchema]) -> List[InvoiceSchema]:
    today = datetime.today()
    due_invoices = []
    for invoice in data:
        try:
            due_date = datetime.strptime(
                invoice.due_date, "%d-%m-%Y")
            if due_date <= today:
                due_invoices.append(invoice)
        except ValueError:
            print(
                f"Invalid date {invoice.id}: {invoice.due_date}")
    return due_invoices


async def download_invoice(session, invoice: InvoiceSchema) -> None:
    """Download a single invoice."""
    try:
        async with session.get(invoice.url, ssl=False) as response:
            if response.status == 200:
                path = os.path.join(INVOICES_DIR, f"{invoice.id}.jpg")
                async with aiofiles.open(path, 'wb') as f:
                    await f.write(await response.read())
    except Exception as e:
        print(f"Failed to download {invoice.id}: {e}")


async def download_all_invoices(data: List[InvoiceSchema]) -> None:
    """Download all invoices."""
    filtered_data = filter_invoices_by_due_date(data)
    os.makedirs(INVOICES_DIR, exist_ok=True)
    async with aiohttp.ClientSession() as session:
        tasks = [download_invoice(session, invoice)
                 for invoice in filtered_data]
        await asyncio.gather(*tasks)


def export_csv(data: List[InvoiceSchema]) -> None:
    """Export data to CSV."""
    filtered_data = filter_invoices_by_due_date(data)
    dict_list = [invoice.model_dump() for invoice in filtered_data]
    df = pd.DataFrame(dict_list)
    csv_path = os.path.join(INVOICES_DIR, "invoices.csv")
    print(csv_path)
    df.to_csv(csv_path, index=False, encoding='utf-8')


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
