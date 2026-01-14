from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field

class InvoiceIn(BaseModel):
    invoiceNumber: str = Field(min_length=1, max_length=50)
    clientName: str = Field(min_length=1, max_length=120)
    issueDate: date
    dueDate: date
    currency: str = Field(min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")
    subtotal: Decimal = Field(ge=0)
    tax: Decimal = Field(ge=0)
    total: Decimal | None = None
    status: str = Field(min_length=1, max_length=30)
    notes: str | None = Field(default=None, max_length=500)

class ValidationResult(BaseModel):
    isValid: bool
    errors: list[str] = []
    normalizedTotal: Decimal | None = None
