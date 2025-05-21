from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List

from schema.invoice import InvoiceSchema


def scrape(url: str) -> List[InvoiceSchema]:
    """Scrape URL data."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
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
