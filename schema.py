from pydantic import BaseModel


class InvoiceSchema(BaseModel):
    id: str
    vencimento: str
    url: str