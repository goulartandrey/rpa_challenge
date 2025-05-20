from datetime import datetime
import os
import pandas as pd
from typing import List

from schema.invoice import InvoiceSchema

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVOICES_DIR = os.path.join(BASE_DIR, "..", "invoices")


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


def export_csv(data: List[InvoiceSchema]) -> None:
    """Export data to CSV."""
    filtered_data = filter_invoices_by_due_date(data)
    dict_list = [invoice.model_dump() for invoice in filtered_data]
    df = pd.DataFrame(dict_list)
    csv_path = os.path.join(INVOICES_DIR, "invoices.csv")
    print(csv_path)
    df.to_csv(csv_path, index=False, encoding='utf-8')
