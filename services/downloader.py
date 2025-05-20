import aiohttp
import aiofiles
import asyncio
import os
from typing import List
from schema.invoice import InvoiceSchema

from utils.utils import filter_invoices_by_due_date


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVOICES_DIR = os.path.join(BASE_DIR, "..", "invoices")


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
