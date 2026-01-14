from decimal import Decimal, ROUND_HALF_UP
from .schemas import InvoiceIn, ValidationResult

def _round2(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def validate_invoice(payload: InvoiceIn) -> ValidationResult:
    errors: list[str] = []

    if payload.dueDate < payload.issueDate:
        errors.append("dueDate must be greater than or equal to issueDate")

    computed_total = _round2(payload.subtotal + payload.tax)

    if payload.total is not None:
        if _round2(payload.total) != computed_total:
            errors.append("total does not match subtotal + tax (rounded to 2 decimals)")

    return ValidationResult(
        isValid=len(errors) == 0,
        errors=errors,
        normalizedTotal=computed_total,
    )
