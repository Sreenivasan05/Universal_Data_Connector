"""
API endpoint tests using FastAPI TestClient.
Connectors are mocked so tests run without real data files or Gemini API.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


# ── Shared mock data ──────────────────────────────────────────────────────────

MOCK_CRM = [
    {"customer_id": i, "email": f"u{i}@x.com",
     "created_at": f"2025-0{i}-01T00:00:00", "status": "active"}
    for i in range(1, 4)
]

MOCK_SUPPORT = [
    {"ticket_id": 1, "priority": "high",   "status": "open",
     "created_at": "2026-01-10T00:00:00", "customer_id": 1, "subject": "Bug"},
    {"ticket_id": 2, "priority": "medium", "status": "closed",
     "created_at": "2026-01-09T00:00:00", "customer_id": 2, "subject": "Help"},
]

MOCK_ANALYTICS = [
    {"metric": "daily_active_users", "value": 900,  "date": "2026-02-15"},
    {"metric": "daily_active_users", "value": 1100, "date": "2026-02-16"},
]


@pytest.fixture
def client():
    """
    TestClient with all three connectors mocked.
    Isolates API logic from file I/O and external services.
    """
    with patch("app.connectors.crm_connector.CRMConnector.fetch",       return_value=MOCK_CRM), \
         patch("app.connectors.support_connector.SupportConnector.fetch", return_value=MOCK_SUPPORT), \
         patch("app.connectors.analytics_connector.AnalyticsConnector.fetch", return_value=MOCK_ANALYTICS):
        from app.main import app
        yield TestClient(app)


# ── Health check ──────────────────────────────────────────────────────────────

class TestHealth:
    def test_health_returns_200(self, client):
        res = client.get("/health")
        assert res.status_code == 200

    def test_health_body(self, client):
        res = client.get("/health")
        assert res.json() == {"status": "ok"}


# ── /data/{source} ────────────────────────────────────────────────────────────

class TestDataEndpoint:
    def test_crm_returns_200(self, client):
        res = client.get("/data/crm")
        assert res.status_code == 200

    def test_support_returns_200(self, client):
        res = client.get("/data/support")
        assert res.status_code == 200

    def test_analytics_returns_200(self, client):
        res = client.get("/data/analytics")
        assert res.status_code == 200

    def test_unknown_source_returns_404(self, client):
        res = client.get("/data/unknown_source")
        assert res.status_code == 404

    def test_response_has_data_and_metadata(self, client):
        res = client.get("/data/crm")
        body = res.json()
        assert "data" in body
        assert "metadata" in body

    def test_metadata_fields_present(self, client):
        res = client.get("/data/crm")
        meta = res.json()["metadata"]
        assert "total_results"    in meta
        assert "returned_results" in meta
        assert "data_freshness"   in meta
        assert "data_type"        in meta
        assert "source"           in meta
        assert "context"          in meta

    def test_metadata_source_matches_request(self, client):
        for source in ("crm", "support", "analytics"):
            res = client.get(f"/data/{source}")
            assert res.json()["metadata"]["source"] == source

    def test_limit_query_param_respected(self, client):
        res = client.get("/data/crm?limit=1")
        body = res.json()
        assert body["metadata"]["returned_results"] <= 1

    def test_limit_default_is_10(self, client):
        # Mock returns 3 records, so returned <= 10 (all returned)
        res = client.get("/data/crm")
        assert res.json()["metadata"]["returned_results"] <= 10

    def test_limit_must_be_positive(self, client):
        res = client.get("/data/crm?limit=0")
        assert res.status_code == 422   # Pydantic validation error

    def test_analytics_returns_aggregated(self, client):
        res = client.get("/data/analytics")
        data = res.json()["data"]
        # Voice optimizer should aggregate, not return raw rows
        assert len(data) <= len(MOCK_ANALYTICS)
        if data:
            assert "average" in data[0]

    def test_total_results_reflects_full_dataset(self, client):
        res = client.get("/data/crm?limit=1")
        meta = res.json()["metadata"]
        # total_results = full set, returned_results = limited set
        assert meta["total_results"] >= meta["returned_results"]


# ── /chat/ ────────────────────────────────────────────────────────────────────

class TestChatEndpoint:
    def test_chat_returns_200(self, client):
        with patch("app.services.llm_service.LLMService.run_agent",
                   return_value="Daily active users averaged 1,000."):
            res = client.post("/chat/", json={"query": "Give me analytics metrics"})
            assert res.status_code == 200

    def test_chat_response_field_present(self, client):
        with patch("app.services.llm_service.LLMService.run_agent",
                   return_value="Here is your data."):
            res = client.post("/chat/", json={"query": "Show CRM data"})
            assert "response" in res.json()

    def test_chat_returns_llm_text(self, client):
        expected = "You have 3 active customers."
        with patch("app.services.llm_service.LLMService.run_agent",
                   return_value=expected):
            res = client.post("/chat/", json={"query": "How many customers?"})
            assert res.json()["response"] == expected

    def test_chat_missing_query_returns_422(self, client):
        res = client.post("/chat/", json={})
        assert res.status_code == 422

    def test_chat_rate_limit_returns_429(self, client):
        from google.api_core.exceptions import ResourceExhausted
        with patch("app.services.llm_service.LLMService.run_agent",
                   side_effect=ResourceExhausted("quota exceeded")):
            res = client.post("/chat/", json={"query": "Show me data"})
            assert res.status_code == 429

    def test_chat_internal_error_returns_500(self, client):
        with patch("app.services.llm_service.LLMService.run_agent",
                   side_effect=Exception("unexpected")):
            res = client.post("/chat/", json={"query": "Show me data"})
            assert res.status_code == 500
