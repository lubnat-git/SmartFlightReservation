
from fastapi.testclient import TestClient
from app.main import app
from app.routes import assistant

client = TestClient(app)


def test_assistant_returns_grounded_answer(monkeypatch):
    def mock_assistant(question):
        return {
            "answer": "The supported simulated payment methods are UPI, Card, Net Banking and Cash.",
            "sources": ["travel_faq.txt", "travel_policies.txt"]
        }

    monkeypatch.setattr(
        assistant,
        "ask_travel_assistant",
        mock_assistant
    )

    response = client.post(
        "/assistant/ask",
        json={"question": "What payment methods are supported?"}
    )

    assert response.status_code == 200
    assert "UPI" in response.json()["answer"]
    assert response.json()["sources"] == [
        "travel_faq.txt",
        "travel_policies.txt"
    ]


def test_assistant_rejects_empty_question():
    response = client.post(
        "/assistant/ask",
        json={"question": ""}
    )

    assert response.status_code == 422


def test_assistant_rejects_question_over_1000_characters():
    response = client.post(
        "/assistant/ask",
        json={"question": "A" * 1001}
    )

    assert response.status_code == 422


def test_assistant_handles_unexpected_error(monkeypatch):
    def mock_assistant(question):
        raise RuntimeError("Simulated internal error")

    monkeypatch.setattr(
        assistant,
        "ask_travel_assistant",
        mock_assistant
    )

    response = client.post(
        "/assistant/ask",
        json={"question": "What are the travel policies?"}
    )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "The AI travel assistant encountered an unexpected error."
    )
