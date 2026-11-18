
from fastapi.testclient import TestClient
from app.main import app
from app.routes import agent

client = TestClient(app)


def test_agent_returns_flight_recommendations(monkeypatch):
    def mock_agent(question):
        return {
            "answer": "The cheapest flight is IndiGo 6E201.",
            "flights": [
                {
                    "flight_id": 1,
                    "airline_name": "IndiGo",
                    "flight_number": "6E201",
                    "departure_time": "2026-12-05T08:00:00",
                    "arrival_time": "2026-12-05T10:15:00",
                    "seats_available": 179,
                    "price": 10100,
                    "source_city": "Delhi",
                    "destination_city": "Mumbai"
                }
            ],
            "tools_used": ["search_flights"]
        }

    monkeypatch.setattr(agent, "run_flight_agent", mock_agent)

    response = client.post(
        "/agent/ask",
        json={"question": "Find flights from Delhi to Mumbai"}
    )

    assert response.status_code == 200
    assert response.json()["flights"][0]["flight_number"] == "6E201"
    assert response.json()["tools_used"] == ["search_flights"]


def test_agent_rejects_empty_question():
    response = client.post(
        "/agent/ask",
        json={"question": ""}
    )

    assert response.status_code == 422


def test_agent_rejects_question_over_1000_characters():
    response = client.post(
        "/agent/ask",
        json={"question": "A" * 1001}
    )

    assert response.status_code == 422


def test_agent_handles_unexpected_error(monkeypatch):
    def mock_agent(question):
        raise RuntimeError("Simulated agent error")

    monkeypatch.setattr(agent, "run_flight_agent", mock_agent)

    response = client.post(
        "/agent/ask",
        json={"question": "Find flights from Delhi to Mumbai"}
    )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "The AI flight agent encountered an unexpected error."
    )
