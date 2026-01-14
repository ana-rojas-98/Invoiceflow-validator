from fastapi import FastAPI
from .schemas import InvoiceIn, ValidationResult
from .validator import validate_invoice

app = FastAPI(
    title="InvoiceFlow Validator API",
    version="1.0.0",
    description="Small FastAPI service to validate invoice payloads (dates, currency, totals).",
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/validate", response_model=ValidationResult)
def validate(invoice: InvoiceIn):
    return validate_invoice(invoice)
