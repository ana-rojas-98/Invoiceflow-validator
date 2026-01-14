# Invoiceflow-validator — FastAPI Invoice Validation Service

`invoiceflow-validator` is a small FastAPI microservice that validates invoice payloads using clear business rules (dates, currency format, and totals). It returns a simple validation result and a normalized total. The API includes automatic Swagger docs and integration tests with `pytest`.

## Features

- Validate invoice payloads with business rules
- Currency format check (3-letter ISO style, e.g., `USD`, `COP`)
- Date validation (`dueDate` must be >= `issueDate`)
- Total normalization (`subtotal + tax`, rounded to 2 decimals)
- Swagger/OpenAPI docs (`/docs`)
- Tests with `pytest`

## Tech Stack

- **Python** (FastAPI + Uvicorn)
- **Pydantic** for request validation
- **pytest** for tests
- **Docker** (optional, for containerized run)
- **GitHub Actions** CI (optional)

---

## Project Structure

```text
invoiceflow-validator/
  app/
    __init__.py
    main.py
    schemas.py
    validator.py
  tests/
    conftest.py
    test_validate.py
  requirements.txt
  Dockerfile
  README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+ (recommended: 3.12)
- `pip`

### Setup (virtual environment)

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> Tip: Always activate `.venv` before running tests or starting the server.

---

## Run the API locally

```bash
uvicorn app.main:app --reload --port 8000
```

Open Swagger docs:

- http://localhost:8000/docs

Health check:

- http://localhost:8000/health

---

## API Endpoints

### Health

`GET /health`

Response:

```json
{ "status": "ok" }
```

### Validate invoice

`POST /validate`

Example request body:

```json
{
  "invoiceNumber": "INV-2026-0001",
  "clientName": "ACME Corp",
  "issueDate": "2026-01-13",
  "dueDate": "2026-02-12",
  "currency": "USD",
  "subtotal": 1000.00,
  "tax": 190.00,
  "total": 1190.00,
  "status": "draft",
  "notes": "Demo invoice"
}
```

Example response:

```json
{
  "isValid": true,
  "errors": [],
  "normalizedTotal": "1190.00"
}
```

If there are issues (for example, wrong total or dates), `isValid` becomes `false` and `errors` will contain messages.

---

## Run Tests

```bash
pytest -q
```

---

## Run with Docker (optional)

Build:

```bash
docker build -t invoiceflow-validator .
```

Run:

```bash
docker run -p 8000:8000 invoiceflow-validator
```

Swagger:

- http://localhost:8000/docs

---

## Roadmap (Next Improvements)

- Add more validation rules (status enum, currency list, etc.)
- Add CI workflow (lint + tests)
- Connect with the .NET InvoiceFlow API as a validation microservice
- Deploy to a cloud platform and expose a public Swagger URL
