from pydantic import BaseModel


class InvoiceSchema(BaseModel):
    id: str
    due_date: str
    url: str
