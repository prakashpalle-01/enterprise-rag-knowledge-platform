from fastapi.testclient import TestClient

from src.main import app


def test_health_check() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_knowledge_ingest_and_search() -> None:
    client = TestClient(app)
    ingest_response = client.post(
        "/knowledge",
        json={
            "item_id": "policy-001",
            "title": "Access Control Policy",
            "body": "All enterprise users must authenticate with MFA before accessing privileged systems.",
        },
    )
    assert ingest_response.status_code == 200
    assert ingest_response.json()["item_id"] == "policy-001"

    search_response = client.post("/search", json={"question": "What is required before privileged access?"})
    assert search_response.status_code == 200
    payload = search_response.json()
    assert payload["matches"]
    assert "privileged" in payload["answer"].lower()
