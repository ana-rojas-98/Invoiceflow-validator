from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_validate_ok_when_total_matches():
    payload = {
        "invoiceNumber": "INV-1",
        "clientName": "ACME",
        "issueDate": "2026-01-13",
        "dueDate": "2026-02-01",
        "currency": "USD",
        "subtotal": 1000.00,
        "tax": 190.00,
        "total": 1190.00,
        "status": "draft",
        "notes": "test"
    }
    r = client.post("/validate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["isValid"] is True
    assert body["errors"] == []
    assert body["normalizedTotal"] == "1190.00"

def test_validate_fails_when_due_date_before_issue_date():
    payload = {
        "invoiceNumber": "INV-2",
        "clientName": "ACME",
        "issueDate": "2026-01-13",
        "dueDate": "2026-01-01",
        "currency": "USD",
        "subtotal": 10,
        "tax": 0,
        "status": "draft"
    }
    r = client.post("/validate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["isValid"] is False
    assert "dueDate must be greater than or equal to issueDate" in body["errors"]
